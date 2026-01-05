const API_URL = "http://localhost:5050";

// --- UI ELEMENTS ---
const elements = {
    chatMessages: document.getElementById('chat-messages'),
    userInput: document.getElementById('user-input'),
    sendBtn: document.getElementById('send-btn'),
    statRequests: document.getElementById('stat-requests'),
    statTokens: document.getElementById('stat-tokens'),
    statL2Tokens: document.getElementById('stat-l2-tokens'),
    statVram: document.getElementById('stat-vram'),
    vramBar: document.getElementById('vram-bar'),
    detailedStatus: document.getElementById('detailed-status'),
    modelInput: document.getElementById('model-name'),
    pullBtn: document.getElementById('pull-btn'),
    ingestBtn: document.getElementById('ingest-btn'),
    clearBtn: document.getElementById('clear-btn'),
    healthDots: document.querySelectorAll('.service-item'),
    modeRagBtn: document.getElementById('mode-rag-btn'),
    modeDevBtn: document.getElementById('mode-dev-btn'),
    librarianBtn: document.getElementById('librarian-btn'),
    scoutInput: document.getElementById('scout-query'),
    scoutBtn: document.getElementById('scout-btn'),
    resetBtn: document.getElementById('reset-btn'),
    navDashboard: document.getElementById('nav-dashboard'),
    navBugs: document.getElementById('nav-bugs'),
    viewDashboard: document.getElementById('view-dashboard'),
    viewBugs: document.getElementById('view-bugs'),
    splashScreen: document.getElementById('splash-screen')
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
        }
    } catch (e) { console.error("Stats fetch failed", e); }
}

async function refreshFinancials() {
    try {
        const response = await fetch(`${API_URL}/governance/financials`);
        const data = await response.json();

        if (data.net_savings_usd !== undefined) {
            document.getElementById('stat-savings').innerText = `$${data.net_savings_usd.toFixed(2)}`;
            document.getElementById('stat-roi').innerText = `ROI: ${data.savings_percentage}%`;
        }
    } catch (e) { console.error("Financials fetch failed", e); }
}

/**
 * Updates UI based on health data received from API or SSE.
 */
function updateHealthUI(data) {
    if (data.status === "success") {
        const h = data.health;

        // 1. Update Detailed Status Text
        const isInitializing = h.ollama === 'offline' || h.qdrant === 'offline';
        const statusText = isInitializing ? 'SYSTEM: INITIALIZING...' : `NVIDIA TITAN RTX: ${h.gpu.percentage}% LOAD`;
        const dotColor = isInitializing ? '#ffaa00' : (h.api === 'online' ? '#107c10' : '#ff4d6d');

        elements.detailedStatus.innerHTML = `<span class="status-dot" style="background: ${dotColor}"></span> ${statusText}`;

        // 2. Update VRAM Stats
        elements.statVram.innerText = `${h.gpu.used}MB / ${h.gpu.total}MB`;
        elements.vramBar.style.width = `${h.gpu.percentage}%`;

        // Adjust bar color based on load
        if (h.gpu.percentage > 90) elements.vramBar.style.background = 'var(--office-danger)';
        else if (h.gpu.percentage > 70) elements.vramBar.style.background = 'var(--office-purple)';
        else elements.vramBar.style.background = 'var(--office-blue)';

        // 3. Update health grid
        elements.healthDots.forEach(item => {
            const service = item.getAttribute('data-service');
            const status = h[service];
            if (status) {
                item.className = `service-item ${status}`;
            }
        });

        // 4. Update Mode Toggle Buttons
        if (data.current_mode === 'RAG') {
            elements.modeRagBtn.classList.add('active');
            elements.modeDevBtn.classList.remove('active');
        } else {
            elements.modeDevBtn.classList.add('active');
            elements.modeRagBtn.classList.remove('active');
        }
    }
}

async function refreshHealth() {
    try {
        const response = await fetch(`${API_URL}/health/detailed`);
        const data = await response.json();
        updateHealthUI(data);
    } catch (e) {
        elements.detailedStatus.innerHTML = `<span class="status-dot" style="background: red;"></span> API OFFLINE`;
    }
}

/**
 * Initializes Server-Sent Events (SSE) for real-time monitoring.
 */
function initHealthStream() {
    console.log("📡 Initializing Nexus Health Stream...");
    const evtSource = new EventSource(`${API_URL}/health/stream`);

    evtSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateHealthUI(data);
    };

    evtSource.onerror = (err) => {
        console.error("SSE connection failed:", err);
        evtSource.close();
        // Fallback to polling if SSE fails
        setTimeout(initHealthStream, 5000);
    };
}

async function toggleSystemMode(targetMode) {
    appendMessage('system', `🔄 SWITCHING ENGINE MODE: [${targetMode}]...`);
    try {
        const response = await fetch(`${API_URL}/system/mode`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: targetMode })
        });
        const data = await response.json();
        if (data.status === 'success') {
            showNotify(`✅ System switched to ${targetMode}`);
            refreshHealth();
        } else {
            showNotify(`❌ Failed: ${data.message}`, true);
        }
    } catch (e) {
        showNotify(`❌ Error: ${e.message}`, true);
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

    const prefix = role === 'user' ? '[USER]' : (role === 'system' ? '[SYSTEM]' : '[AI]');
    let color = 'var(--neon-purple)';
    if (role === 'user') color = 'var(--neon-blue)';
    if (role === 'system') color = '#888';

    div.innerHTML = `<span class="prefix" style="color: ${color}">${prefix}</span> ${content}`;

    elements.chatMessages.appendChild(div);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    return id;
}

function updateMessage(id, content, layer = null) {
    const div = document.getElementById(`msg-${id}`);
    if (!div) return;

    // Reset content area (keep prefix if it exists)
    const prefixSpan = div.querySelector('.prefix');
    const prefixHTML = prefixSpan ? prefixSpan.outerHTML + ' ' : '';

    let reasoningHTML = '';
    let answerText = content;

    // 1. EXTRACT THINKING / REASONING
    const thinkMatch = content.match(/<think>([\s\S]*?)<\/think>/i);
    if (thinkMatch) {
        const reasoning = thinkMatch[1].trim();
        reasoningHTML = `<div class="thinking-block">${reasoning}</div>`;
        answerText = content.replace(/<think>[\s\S]*?<\/think>/i, '').trim();
    }

    // 2. RENDER MARKDOWN
    let renderedAnswer = answerText;
    if (window.marked) {
        // Simple markdown parsing
        renderedAnswer = marked.parse(answerText);
    }

    // 3. APPLY TO UI
    div.innerHTML = `
        ${layer ? `<div class="message-badge badge-${layer.toLowerCase()}">${layer.toUpperCase()}</div>` : ''}
        ${prefixHTML}
        ${reasoningHTML}
        <div class="answer-content">${renderedAnswer}</div>
    `;

    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
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

elements.ingestBtn.addEventListener('click', async () => {
    // Show immediate feedback
    const loadingId = appendMessage('system', '🔄 FORCE RE-SCAN INITIATED: Purging old memory...');

    // Start continuous VRAM monitoring during ingestion
    const healthMonitor = setInterval(() => refreshHealth(), 1000);

    try {
        const response = await fetch(`${API_URL}/ingest`, { method: 'POST' });
        const data = await response.json();

        // Stop monitoring
        clearInterval(healthMonitor);

        if (data.status === 'success') {
            const summary = data.summary || {};
            const msg = `✅ INGESTION COMPLETE\n` +
                `📁 Files Processed: ${summary.files_processed || 0}\n` +
                `📄 Chunks Ingested: ${summary.chunks_ingested || 0}\n` +
                `⏱️ Memory refreshed and ready for queries.`;
            updateMessage(loadingId, msg);

            // Final refresh to show updated state
            setTimeout(() => {
                refreshHealth();
                refreshStats();
            }, 1000);
        } else {
            updateMessage(loadingId, `❌ INGESTION FAILED: ${data.message || 'Unknown error'}`);
        }
    } catch (e) {
        // Stop monitoring on error
        clearInterval(healthMonitor);
        updateMessage(loadingId, `❌ CONNECTION ERROR: ${e.message}`);
    }
});
elements.clearBtn.addEventListener('click', () => {
    if (confirm("Permanently wipe short-term memory?")) {
        handleAction('/history', 'DELETE');
    }
});

elements.modeRagBtn.addEventListener('click', () => toggleSystemMode('RAG'));
elements.modeDevBtn.addEventListener('click', () => toggleSystemMode('DEV'));

elements.librarianBtn.addEventListener('click', async () => {
    appendMessage('system', "🧹 STARTING LIBRARIAN (NIGHT SHIFT)...");
    try {
        const response = await fetch(`${API_URL}/agents/librarian/run`, { method: 'POST' });
        const data = await response.json();
        if (data.status === 'success') {
            appendMessage('system', `✅ LIBRARIAN FINISHED: Processed ${data.files_processed} files.`);
        } else {
            appendMessage('system', `❌ LIBRARIAN FAILED: ${data.message || 'Unknown error'}`);
        }
    } catch (e) {
        appendMessage('system', `❌ ERROR: ${e.message}`);
    }
});

elements.scoutBtn.addEventListener('click', async () => {
    const query = elements.scoutInput.value.trim();
    if (!query) return;

    appendMessage('system', `🔭 DEPLOYING SCOUT FOR: "${query}"...`);
    elements.scoutInput.value = "";

    const loadingId = appendMessage('ai', "📑 SCOUT IS RESEARCHING & SYNTHESIZING...");

    try {
        const response = await fetch(`${API_URL}/agents/scout/research`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await response.json();
        if (data.status === 'success') {
            updateMessage(loadingId, data.report, "L3");
        } else {
            updateMessage(loadingId, `❌ SCOUT FAILED: ${data.message || 'Unknown error'}`);
        }
    } catch (e) {
        updateMessage(loadingId, `❌ ERROR: ${e.message}`);
    }
});

elements.resetBtn.addEventListener('click', () => {
    if (confirm("⚠️ WARNING: This will restart all Gravitas containers and clear transient states. Proceed?")) {
        handleAction('/system/reset');
        appendMessage('system', "🚨 HARD SYSTEM RESET INITIATED. Expect downtime...");
    }
});

// --- NAVIGATION ---
function switchView(viewName) {
    if (viewName === 'dashboard') {
        elements.viewDashboard.style.display = 'grid';
        elements.viewBugs.style.display = 'none';
        elements.navDashboard.classList.add('active');
        elements.navBugs.classList.remove('active');
    } else {
        elements.viewDashboard.style.display = 'none';
        elements.viewBugs.style.display = 'grid';
        elements.navBugs.classList.add('active');
        elements.navDashboard.classList.remove('active');
    }
}

elements.navDashboard.addEventListener('click', () => switchView('dashboard'));
elements.navBugs.addEventListener('click', () => switchView('bugs'));

// --- SPLASH CONTROL ---
function initSplash() {
    setTimeout(() => {
        elements.splashScreen.style.opacity = '0';
        setTimeout(() => {
            elements.splashScreen.style.visibility = 'hidden';
        }, 1000);
    }, 3000);
}

// --- INITIALIZE ---
initSplash();
refreshStats();
initHealthStream();
refreshFinancials();
setInterval(refreshStats, 5000);
setInterval(refreshFinancials, 30000); // ROI updates every 30s
