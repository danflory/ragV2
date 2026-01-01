const API_URL = "http://localhost:5050";

// --- UI ELEMENTS ---
const elements = {
    chatMessages: document.getElementById('chat-messages'),
    userInput: document.getElementById('user-input'),
    sendBtn: document.getElementById('send-btn'),
    statRequests: document.getElementById('stat-requests'),
    statTokens: document.getElementById('stat-tokens'),
    statL2Tokens: document.getElementById('stat-l2-tokens'),
    statLatency: document.getElementById('stat-latency'),
    detailedStatus: document.getElementById('detailed-status'),
    modelInput: document.getElementById('model-name'),
    pullBtn: document.getElementById('pull-btn'),
    ingestBtn: document.getElementById('ingest-btn'),
    clearBtn: document.getElementById('clear-btn'),
    healthDots: document.querySelectorAll('.service-item')
};

// --- CORE LOGIC ---

async function triggerChat() {
    const text = elements.userInput.value.trim();
    if (!text) return;

    // Add user message to UI
    appendMessage('user', text);
    elements.userInput.value = "";

    // Add loading indicator
    const loadingId = appendMessage('ai', "📡 PROCESSING...");

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        updateMessage(loadingId, data.response, data.layer);

        // Refresh stats after a chat
        refreshStats();
    } catch (error) {
        updateMessage(loadingId, `❌ CONNECTION FAILED: ${error.message}`);
    }
}

async function refreshStats() {
    try {
        const response = await fetch(`${API_URL}/stats/summary`);
        const data = await response.json();

        if (data.status === "success") {
            const { summary } = data;
            elements.statRequests.innerText = summary.total_requests;
            elements.statTokens.innerText = summary.total_tokens.toLocaleString();
            elements.statL2Tokens.innerText = summary.l2_tokens ? summary.l2_tokens.toLocaleString() : '0';
            elements.statLatency.innerText = `${Math.round(summary.avg_latency_ms)}ms`;
        }
    } catch (e) { console.error("Stats fetch failed", e); }
}

async function refreshHealth() {
    try {
        const response = await fetch(`${API_URL}/health/detailed`);
        const data = await response.json();

        if (data.status === "success") {
            const h = data.health;

            // Update HUD status
            elements.detailedStatus.innerHTML = `<span class="status-dot"></span> NVIDIA TITAN RTX: ONLINE`;

            // Update health grid
            elements.healthDots.forEach(item => {
                const service = item.getAttribute('data-service');
                const status = h[service];
                item.className = `service-item ${status}`;
            });
        }
    } catch (e) {
        elements.detailedStatus.innerHTML = `<span class="status-dot" style="background: red;"></span> API OFFLINE`;
    }
}

async function handleAction(endpoint, method = 'POST', payload = null) {
    try {
        const config = { method, headers: { 'Content-Type': 'application/json' } };
        if (payload) config.body = JSON.stringify(payload);

        const response = await fetch(`${API_URL}${endpoint}`, config);
        const data = await response.json();

        if (data.status === "success") {
            showNotify(`✅ ${data.message}`);
        } else {
            showNotify(`❌ ${data.message}`, true);
        }
    } catch (e) {
        showNotify(`❌ Error: ${e.message}`, true);
    }
}

// --- HELPERS ---

function appendMessage(role, content) {
    const id = Date.now();
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.id = `msg-${id}`;

    const prefix = role === 'user' ? '[USER]' : '[AI]';
    div.innerHTML = `<span class="prefix" style="color: ${role === 'user' ? 'var(--neon-blue)' : 'var(--neon-purple)'}">${prefix}</span> ${content}`;

    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    return id;
}

function updateMessage(id, content, layer = null) {
    const div = document.getElementById(`msg-${id}`);
    if (div) {
        div.innerHTML = div.innerHTML.split('</span>')[0] + '</span> ' + content;

        if (layer) {
            const badge = document.createElement('div');
            badge.className = `message-badge badge-${layer.toLowerCase()}`;
            badge.innerText = layer.toUpperCase();
            div.prepend(badge);
        }
    }
}

function showNotify(text, isError = false) {
    const div = document.createElement('div');
    div.className = 'message system';
    div.style.border = isError ? '1px solid #ff0055' : '1px solid var(--neon-blue)';
    div.innerText = text;
    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

// --- EVENT LISTENERS ---

elements.sendBtn.addEventListener('click', triggerChat);
elements.userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') triggerChat(); });

elements.pullBtn.addEventListener('click', () => {
    const model = elements.modelInput.value;
    if (model) handleAction('/model/pull', 'POST', { model });
});

elements.ingestBtn.addEventListener('click', () => handleAction('/ingest'));
elements.clearBtn.addEventListener('click', () => {
    if (confirm("Permanently wipe short-term memory?")) {
        handleAction('/history', 'DELETE');
    }
});

// --- INITIALIZE ---
refreshStats();
refreshHealth();
setInterval(refreshStats, 5000);
setInterval(refreshHealth, 10000);
