(() => {

  // ══════════════════════════════════════════════
  // STORE PRODUCT DATA
  // ══════════════════════════════════════════════
  const PRODUCTS = [
    { name: "Classic White Tee",        category: "Men's",       emoji: "👕", price: 29.99, gradient: "linear-gradient(135deg,#f8fafc,#e2e8f0)", sale: false },
    { name: "Slim Fit Jeans",           category: "Men's",       emoji: "👖", price: 79.99, gradient: "linear-gradient(135deg,#dbeafe,#93c5fd)", sale: false },
    { name: "Zip Hoodie",               category: "Men's",       emoji: "🧥", price: 59.99, gradient: "linear-gradient(135deg,#fef3c7,#fde68a)", sale: false },
    { name: "Leather Jacket",           category: "Men's",       emoji: "🧥", price: 149.99, originalPrice: 199.99, gradient: "linear-gradient(135deg,#1e293b,#475569)", sale: true },
    { name: "Floral Dress",             category: "Women's",     emoji: "👗", price: 89.99, gradient: "linear-gradient(135deg,#fce7f3,#f9a8d4)", sale: false },
    { name: "Silk Blouse",              category: "Women's",     emoji: "👚", price: 69.99, gradient: "linear-gradient(135deg,#ede9fe,#c4b5fd)", sale: false },
    { name: "High-Waist Skirt",         category: "Women's",     emoji: "👗", price: 54.99, originalPrice: 74.99, gradient: "linear-gradient(135deg,#fef9c3,#fef08a)", sale: true },
    { name: "Ankle Boots",              category: "Women's",     emoji: "👢", price: 119.99, gradient: "linear-gradient(135deg,#d1fae5,#6ee7b7)", sale: false },
    { name: "Leather Handbag",          category: "Accessories", emoji: "👜", price: 99.99, gradient: "linear-gradient(135deg,#fee2e2,#fca5a5)", sale: false },
    { name: "Minimalist Watch",         category: "Accessories", emoji: "⌚", price: 189.99, originalPrice: 249.99, gradient: "linear-gradient(135deg,#e0f2fe,#7dd3fc)", sale: true },
    { name: "Retro Sunglasses",         category: "Accessories", emoji: "🕶️", price: 39.99, gradient: "linear-gradient(135deg,#f0fdf4,#86efac)", sale: false },
    { name: "Baseball Cap",             category: "Accessories", emoji: "🧢", price: 24.99, gradient: "linear-gradient(135deg,#fff7ed,#fdba74)", sale: false },
  ];

  let cartCount = 0;

  // ══════════════════════════════════════════════
  // TAB SWITCHING
  // ══════════════════════════════════════════════
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
  });

  // ══════════════════════════════════════════════
  // STORE — product rendering & filters
  // ══════════════════════════════════════════════
  function renderProducts(filter) {
    const grid = document.getElementById('store-grid');
    const title = document.getElementById('store-section-title');
    const countEl = document.getElementById('store-product-count');

    const filtered = filter === 'all'
      ? PRODUCTS
      : filter === 'Sale'
      ? PRODUCTS.filter(p => p.sale)
      : PRODUCTS.filter(p => p.category === filter);

    title.textContent = filter === 'all' ? 'All Products'
      : filter === 'Sale' ? '🔥 On Sale'
      : filter;
    countEl.textContent = `${filtered.length} items`;

    grid.innerHTML = filtered.map((p, i) => `
      <div class="product-card" data-index="${i}">
        <div class="product-img" style="background:${p.gradient}">
          ${p.sale ? '<span class="product-sale-badge">SALE</span>' : ''}
          <span>${p.emoji}</span>
        </div>
        <div class="product-info">
          <div class="product-cat">${p.category}</div>
          <div class="product-name">${p.name}</div>
          <div class="product-footer">
            <div class="product-price">
              $${p.price.toFixed(2)}
              ${p.originalPrice ? `<span class="original">$${p.originalPrice.toFixed(2)}</span>` : ''}
            </div>
            <button class="btn-cart" data-name="${p.name}">+ Cart</button>
          </div>
        </div>
      </div>
    `).join('');

    // Add to cart buttons
    grid.querySelectorAll('.btn-cart').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        cartCount++;
        document.getElementById('cart-count').textContent = cartCount;
        btn.textContent = '✓ Added';
        btn.classList.add('added');
        setTimeout(() => { btn.textContent = '+ Cart'; btn.classList.remove('added'); }, 1400);
      });
    });
  }

  // Store filter buttons
  document.querySelectorAll('.store-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.store-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderProducts(btn.dataset.filter);
    });
  });

  // Hero "Shop Now" button
  document.querySelector('.store-hero-btn')?.addEventListener('click', () => {
    document.querySelectorAll('.store-filter').forEach(b => b.classList.remove('active'));
    document.querySelector('.store-filter[data-filter="all"]').classList.add('active');
    renderProducts('all');
    document.querySelector('.store-body').scrollIntoView({ behavior: 'smooth' });
  });

  // Initial render
  renderProducts('all');

  // ══════════════════════════════════════════════
  // ADMIN DASHBOARD DATA
  // ══════════════════════════════════════════════
  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  async function loadStats() {
    try {
      const data = await fetch('/api/data/stats').then(r => r.json());
      document.getElementById('stat-orders').textContent    = data.total_orders;
      document.getElementById('stat-revenue').textContent   = '$' + data.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2 });
      document.getElementById('stat-pending').textContent   = data.pending;
      document.getElementById('stat-delivered').textContent = data.delivered;
      document.getElementById('stat-customers').textContent = data.total_customers;
    } catch {}
  }

  async function loadOrders() {
    try {
      const orders = await fetch('/api/data/orders').then(r => r.json());
      document.getElementById('orders-count').textContent = `${orders.length} records`;
      document.getElementById('orders-body').innerHTML = orders.map(o => `
        <tr>
          <td><span class="order-id">${esc(o.id)}</span></td>
          <td>${esc(o.customer)}</td>
          <td>${esc(o.product)}</td>
          <td>$${o.amount.toFixed(2)}</td>
          <td>${esc(o.date)}</td>
          <td><span class="badge-status badge-${esc(o.status)}">${esc(o.status)}</span></td>
        </tr>`).join('');
    } catch {
      document.getElementById('orders-body').innerHTML = '<tr><td colspan="6" class="loading">Failed to load.</td></tr>';
    }
  }

  async function loadCustomers() {
    try {
      const customers = await fetch('/api/data/customers').then(r => r.json());
      document.getElementById('customers-count').textContent = `${customers.length} records`;
      document.getElementById('customers-body').innerHTML = customers.map(c => `
        <tr>
          <td><strong>${esc(c.name)}</strong></td>
          <td>${esc(c.email)}</td>
          <td>${esc(c.location)}</td>
          <td>${esc(c.joined)}</td>
          <td>${c.orders}</td>
          <td>$${c.total_spent.toFixed(2)}</td>
        </tr>`).join('');
    } catch {
      document.getElementById('customers-body').innerHTML = '<tr><td colspan="6" class="loading">Failed to load.</td></tr>';
    }
  }

  // ══════════════════════════════════════════════
  // FLOATING CHAT WIDGET
  // ══════════════════════════════════════════════
  let sessionId = null;
  let isWaiting = false;
  let panelOpen = false;

  const chatToggle = document.getElementById('chat-toggle');
  const chatPanel  = document.getElementById('chat-panel');
  const chatClose  = document.getElementById('chat-close');
  const leadView   = document.getElementById('dp-lead-view');
  const leadForm   = document.getElementById('dp-lead-form');
  const formError  = document.getElementById('dp-form-error');
  const startBtn   = document.getElementById('dp-start-btn');
  const chatView   = document.getElementById('dp-chat-view');
  const messages   = document.getElementById('dp-messages');
  const dpInput    = document.getElementById('dp-input');
  const sendBtn    = document.getElementById('dp-send');

  function openPanel() {
    panelOpen = true;
    chatPanel.classList.add('open');
    chatPanel.setAttribute('aria-hidden', 'false');
    document.getElementById('chat-toggle-icon').textContent = '✕';
    if (sessionId) dpInput.focus();
    else document.getElementById('dp-name').focus();
  }
  function closePanel() {
    panelOpen = false;
    chatPanel.classList.remove('open');
    chatPanel.setAttribute('aria-hidden', 'true');
    document.getElementById('chat-toggle-icon').textContent = '💬';
  }

  chatToggle.addEventListener('click', () => panelOpen ? closePanel() : openPanel());
  chatClose.addEventListener('click', closePanel);

  leadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name  = document.getElementById('dp-name').value.trim();
    const email = document.getElementById('dp-email').value.trim();
    startBtn.disabled = true;
    startBtn.textContent = 'Starting…';
    formError.classList.add('hidden');
    try {
      const res = await fetch('/leads', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      });
      if (!res.ok) throw new Error();
      sessionId = (await res.json()).session_id;
      leadView.classList.add('hidden');
      chatView.classList.remove('hidden');
      appendBubble('bot', `Hi ${name}! I'm your AI support assistant.\n\nI can answer questions about the data in this demo — try:\n• "How many pending orders?"\n• "What's the status of ORD-007?"\n• "Who is the top customer?"`);
      dpInput.focus();
    } catch {
      formError.textContent = 'Could not start chat. Please try again.';
      formError.classList.remove('hidden');
      startBtn.disabled = false;
      startBtn.textContent = 'Start Chat';
    }
  });

  async function sendMessage() {
    if (isWaiting) return;
    const text = dpInput.value.trim();
    if (!text) return;
    dpInput.value = '';
    appendBubble('user', text);
    setWaiting(true);
    const typingId = appendTyping();
    try {
      const res = await fetch('/demo/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      });
      removeBubble(typingId);
      if (!res.ok) { appendBubble('bot', 'Sorry, something went wrong.'); return; }
      appendBubble('bot', (await res.json()).reply);
    } catch {
      removeBubble(typingId);
      appendBubble('bot', 'Network error — check your connection.');
    } finally { setWaiting(false); }
  }

  sendBtn.addEventListener('click', sendMessage);
  dpInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  });

  function appendBubble(role, text) {
    const div = document.createElement('div');
    div.className = `dp-bubble ${role}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }
  function appendTyping() {
    const id = `t-${Date.now()}`;
    const div = document.createElement('div');
    div.id = id; div.className = 'dp-bubble bot typing'; div.textContent = '…';
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return id;
  }
  function removeBubble(id) { document.getElementById(id)?.remove(); }
  function setWaiting(s) { isWaiting = s; sendBtn.disabled = s; dpInput.disabled = s; }

  // ── Init ─────────────────────────────────────
  loadStats();
  loadOrders();
  loadCustomers();

})();
