import sqlite3
import uuid
from contextlib import asynccontextmanager
from contextvars import ContextVar
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from data import CUSTOMERS, ORDERS

load_dotenv()

DB_PATH = Path("leads.db")
STATIC_DIR = Path("static")

_current_session: ContextVar[str] = ContextVar("current_session", default="")
conversations: dict[str, list[dict]] = {}

# ── System prompts ─────────────────────────────────────────────────────────

SUPPORT_SYSTEM_PROMPT = (
    "You are a friendly and knowledgeable customer support assistant for a demo business. "
    "Help visitors with their questions, provide accurate information, and use your tools when needed. "
    "If a visitor's issue cannot be resolved through conversation, use the escalate_to_human tool. "
    "Keep responses concise — 1 to 3 short paragraphs. Never make up facts you are not certain about."
)

DEMO_SYSTEM_PROMPT = (
    "You are an intelligent customer support assistant for ShopBot, a demo e-commerce store. "
    "You have access to real store data — orders, customers, and products. "
    "Always use your tools to look up accurate data before answering questions about orders or customers. "
    "Be concise and helpful. If an issue cannot be resolved, use the escalate_to_human tool."
)

FAQ: dict[str, str] = {
    "hours":    "Our support team is available Monday–Friday, 9 AM–6 PM EST.",
    "return":   "We offer a 30-day hassle-free return policy. Contact support to initiate a return.",
    "shipping": "Standard shipping takes 3–5 business days. Express shipping (1–2 days) is available at checkout.",
    "pricing":  "Pricing varies by product. You can browse our full catalog in the Products section.",
    "contact":  "You can reach us at support@shopbot-demo.com or via this chat.",
    "refund":   "Refunds are processed within 5–7 business days after we receive the returned item.",
    "cancel":   "You can cancel your subscription at any time from your account dashboard with no penalty.",
    "password": "Click 'Forgot Password' on the login page to reset your password via email.",
    "account":  "You can update your account details from the Profile section after logging in.",
}

# ── Shared tools ───────────────────────────────────────────────────────────

@tool
def search_faq(query: str) -> str:
    """Search the business FAQ for an answer to the visitor's question."""
    q = query.lower()
    for keyword, answer in FAQ.items():
        if keyword in q:
            return answer
    return "I don't have specific information on that topic in our FAQ."


@tool
def escalate_to_human(issue_summary: str) -> str:
    """Escalate an unresolved issue to a human agent. Call this when you cannot solve the visitor's problem."""
    session_id = _current_session.get()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO escalations (session_id, issue_summary) VALUES (?, ?)",
            (session_id, issue_summary),
        )
        conn.commit()
    finally:
        conn.close()
    return (
        "I've flagged your issue for a human agent. "
        "Someone will follow up at the email address you provided when you started the chat."
    )


# ── Demo-only tools (data-aware) ───────────────────────────────────────────

@tool
def get_store_stats() -> str:
    """Get summary statistics: total orders, revenue, order counts by status, and top customer by spend."""
    total_revenue = sum(o["amount"] for o in ORDERS)
    by_status: dict[str, int] = {}
    spend_by_customer: dict[str, float] = {}
    for o in ORDERS:
        by_status[o["status"]] = by_status.get(o["status"], 0) + 1
        spend_by_customer[o["customer"]] = spend_by_customer.get(o["customer"], 0.0) + o["amount"]

    top = max(spend_by_customer, key=spend_by_customer.get)  # type: ignore[arg-type]
    lines = [
        f"Total orders: {len(ORDERS)}",
        f"Total revenue: ${total_revenue:,.2f}",
        *[f"{status} orders: {count}" for status, count in sorted(by_status.items())],
        f"Top customer by spend: {top} (${spend_by_customer[top]:,.2f})",
    ]
    return "\n".join(lines)


@tool
def get_orders(status: str = "", customer_name: str = "") -> str:
    """
    List orders, optionally filtered by status (Pending/Shipped/Delivered/Cancelled)
    or by customer name (partial match). Returns a summary of each matching order.
    """
    results = ORDERS
    if status:
        results = [o for o in results if o["status"].lower() == status.lower()]
    if customer_name:
        results = [o for o in results if customer_name.lower() in o["customer"].lower()]
    if not results:
        return "No orders found matching those filters."
    lines = [
        f"{o['id']}: {o['customer']} — {o['product']} — ${o['amount']} — {o['status']} ({o['date']})"
        for o in results
    ]
    return f"Found {len(results)} order(s):\n" + "\n".join(lines)


@tool
def get_order_details(order_id: str) -> str:
    """Look up the full details of a specific order by its ID (e.g. ORD-007)."""
    oid = order_id.upper().strip()
    for o in ORDERS:
        if o["id"] == oid:
            return (
                f"Order {o['id']}:\n"
                f"  Customer: {o['customer']}\n"
                f"  Product:  {o['product']}\n"
                f"  Amount:   ${o['amount']}\n"
                f"  Status:   {o['status']}\n"
                f"  Date:     {o['date']}"
            )
    return f"No order found with ID {order_id}."


@tool
def get_customer_details(customer_name: str) -> str:
    """Look up a customer's profile and order history by name (partial match supported)."""
    matches = [c for c in CUSTOMERS if customer_name.lower() in c["name"].lower()]
    if not matches:
        return f"No customer found matching '{customer_name}'."
    lines = []
    for c in matches:
        cust_orders = [o for o in ORDERS if o["customer"] == c["name"]]
        order_list = ", ".join(f"{o['id']} ({o['status']})" for o in cust_orders) or "none"
        lines.append(
            f"{c['name']} | {c['email']} | {c['location']} | "
            f"Joined: {c['joined']} | Orders: {c['orders']} | Spent: ${c['total_spent']:,.2f}\n"
            f"  Orders: {order_list}"
        )
    return "\n\n".join(lines)


# ── Agents ─────────────────────────────────────────────────────────────────

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

support_agent = create_react_agent(
    llm,
    tools=[search_faq, escalate_to_human],
    prompt=SUPPORT_SYSTEM_PROMPT,
)

demo_agent = create_react_agent(
    llm,
    tools=[get_store_stats, get_orders, get_order_details, get_customer_details, search_faq, escalate_to_human],
    prompt=DEMO_SYSTEM_PROMPT,
)


# ── DB ─────────────────────────────────────────────────────────────────────

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL,
                captured_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS escalations (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id    TEXT    NOT NULL,
                issue_summary TEXT    NOT NULL,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ── Pages ──────────────────────────────────────────────────────────────────

@app.get("/")
def serve_landing():
    return FileResponse(STATIC_DIR / "landing.html")


@app.get("/demo")
def serve_demo():
    return FileResponse(STATIC_DIR / "demo.html")


# ── Data API (powers demo dashboard tables) ────────────────────────────────

@app.get("/api/data/orders")
def api_orders():
    return JSONResponse(ORDERS)


@app.get("/api/data/customers")
def api_customers():
    return JSONResponse(CUSTOMERS)


@app.get("/api/data/stats")
def api_stats():
    total_revenue = sum(o["amount"] for o in ORDERS)
    return JSONResponse({
        "total_orders":    len(ORDERS),
        "total_revenue":   round(total_revenue, 2),
        "pending":         sum(1 for o in ORDERS if o["status"] == "Pending"),
        "delivered":       sum(1 for o in ORDERS if o["status"] == "Delivered"),
        "total_customers": len(CUSTOMERS),
    })


# ── Lead capture ──────────────────────────────────────────────────────────

class LeadIn(BaseModel):
    name: str
    email: str


@app.post("/leads", status_code=201)
def create_lead(lead: LeadIn):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO leads (name, email) VALUES (?, ?)",
            (lead.name.strip(), lead.email.strip().lower()),
        )
        conn.commit()
    finally:
        conn.close()
    session_id = str(uuid.uuid4())
    conversations[session_id] = []
    return {"session_id": session_id}


# ── Chat helper ────────────────────────────────────────────────────────────

class ChatIn(BaseModel):
    session_id: str
    message: str


def run_agent(agent, session_id: str, message: str) -> str:
    history = conversations.get(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    token = _current_session.set(session_id)
    messages: list = [
        HumanMessage(content=e["content"]) if e["type"] == "human" else AIMessage(content=e["content"])
        for e in history
    ]
    messages.append(HumanMessage(content=message.strip()))

    try:
        result = agent.invoke({"messages": messages})
    finally:
        _current_session.reset(token)

    reply = ""
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            reply = msg.content
            break

    history.append({"type": "human", "content": message.strip()})
    history.append({"type": "ai",    "content": reply})
    return reply


# ── Chat endpoints ─────────────────────────────────────────────────────────

@app.post("/chat")
def chat(body: ChatIn):
    return {"reply": run_agent(support_agent, body.session_id, body.message)}


@app.post("/demo/chat")
def demo_chat(body: ChatIn):
    return {"reply": run_agent(demo_agent, body.session_id, body.message)}
