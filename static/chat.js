(() => {
  let sessionId = null;
  let isWaiting = false;

  const leadFormView = document.getElementById('lead-form-view');
  const chatView     = document.getElementById('chat-view');
  const leadForm     = document.getElementById('lead-form');
  const formError    = document.getElementById('form-error');
  const startBtn     = document.getElementById('start-btn');
  const messageList  = document.getElementById('message-list');
  const userInput    = document.getElementById('user-input');
  const sendBtn      = document.getElementById('send-btn');
  const greetedName  = document.getElementById('greeted-name');

  // ── Lead form submission ──────────────────────────────────────────────────

  leadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name  = document.getElementById('visitor-name').value.trim();
    const email = document.getElementById('visitor-email').value.trim();

    startBtn.disabled = true;
    startBtn.textContent = 'Starting…';
    formError.classList.add('hidden');

    try {
      const res = await fetch('/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email }),
      });

      if (!res.ok) throw new Error('Server error');

      const data = await res.json();
      sessionId = data.session_id;
      greetedName.textContent = `Hi, ${name}!`;
      switchToChat();
      appendBubble('bot', 'Hello! How can I help you today?');
    } catch {
      formError.textContent = 'Could not start the chat. Please try again.';
      formError.classList.remove('hidden');
      startBtn.disabled = false;
      startBtn.textContent = 'Start Chat';
    }
  });

  // ── View switching ────────────────────────────────────────────────────────

  function switchToChat() {
    leadFormView.classList.add('hidden');
    chatView.classList.remove('hidden');
    userInput.focus();
  }

  // ── Sending messages ──────────────────────────────────────────────────────

  async function sendMessage() {
    if (isWaiting) return;
    const text = userInput.value.trim();
    if (!text) return;

    userInput.value = '';
    appendBubble('user', text);
    setWaiting(true);

    const typingId = appendTyping();

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      });

      removeBubble(typingId);

      if (!res.ok) {
        appendBubble('bot', 'Sorry, something went wrong. Please try again.');
        return;
      }

      const data = await res.json();
      appendBubble('bot', data.reply);
    } catch {
      removeBubble(typingId);
      appendBubble('bot', 'Network error — please check your connection and try again.');
    } finally {
      setWaiting(false);
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // ── UI helpers ────────────────────────────────────────────────────────────

  function appendBubble(role, text) {
    const div = document.createElement('div');
    div.className = `bubble ${role}`;
    div.textContent = text;
    messageList.appendChild(div);
    scrollToBottom();
    return div.id;
  }

  function appendTyping() {
    const id = `typing-${Date.now()}`;
    const div = document.createElement('div');
    div.id = id;
    div.className = 'bubble bot typing';
    div.textContent = '…';
    messageList.appendChild(div);
    scrollToBottom();
    return id;
  }

  function removeBubble(id) {
    document.getElementById(id)?.remove();
  }

  function scrollToBottom() {
    messageList.scrollTop = messageList.scrollHeight;
  }

  function setWaiting(state) {
    isWaiting = state;
    sendBtn.disabled = state;
    userInput.disabled = state;
  }
})();
