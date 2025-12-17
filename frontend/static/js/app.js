/**
 * Company MCP Frontend - JavaScript Application
 * Handles navigation, chat with GPT-4o, file browsing, and MCP server management
 */

// ═══════════════════════════════════════════════════════════════════════════
// State Management
// ═══════════════════════════════════════════════════════════════════════════

const state = {
    currentPage: 'home',
    mcpConnected: false,
    chatHistory: [],
    currentPath: '/data',
    isLoading: false,
    mcpServers: {},
    openaiConfigured: false,
    // Wiki state
    wikiStructure: null,
    wikiExpandedNodes: new Set(),
    wikiSelectedTable: null,
    wikiSearchQuery: '',
    // Chat session state
    currentSessionId: null,
    chatSessions: {},  // { sessionId: { id, title, history, createdAt } }
};

// ═══════════════════════════════════════════════════════════════════════════
// Router - URL-based Navigation
// ═══════════════════════════════════════════════════════════════════════════

const router = {
    routes: {
        '/': 'home',
        '/chat': 'chat',
        '/wiki': 'wiki',
        '/files': 'files',
        '/settings': 'settings',
        '/admin': 'admin',
    },
    
    /**
     * Parse current URL and return page and params
     */
    parseUrl() {
        const path = window.location.pathname;
        
        // Check for chat session: /chat/:sessionId
        const chatSessionMatch = path.match(/^\/chat\/([a-zA-Z0-9_-]+)$/);
        if (chatSessionMatch) {
            return { page: 'chat', sessionId: chatSessionMatch[1] };
        }
        
        // Check standard routes
        const page = this.routes[path];
        if (page) {
            return { page, sessionId: null };
        }
        
        // Default to home
        return { page: 'home', sessionId: null };
    },
    
    /**
     * Build URL for a given page and optional session ID
     */
    buildUrl(page, sessionId = null) {
        if (page === 'chat' && sessionId) {
            return `/chat/${sessionId}`;
        }
        if (page === 'home') {
            return '/';
        }
        return `/${page}`;
    },
    
    /**
     * Navigate to a URL and update browser history
     */
    push(page, sessionId = null, replace = false) {
        const url = this.buildUrl(page, sessionId);
        if (replace) {
            window.history.replaceState({ page, sessionId }, '', url);
        } else {
            window.history.pushState({ page, sessionId }, '', url);
        }
    },
    
    /**
     * Initialize router and handle initial URL
     */
    init() {
        // Handle browser back/forward buttons
        window.addEventListener('popstate', (event) => {
            if (event.state) {
                navigateTo(event.state.page, event.state.sessionId, false);
            } else {
                const { page, sessionId } = this.parseUrl();
                navigateTo(page, sessionId, false);
            }
        });
        
        // Handle initial URL on page load
        const { page, sessionId } = this.parseUrl();
        navigateTo(page, sessionId, true);
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// Navigation
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Navigate to a page with optional session ID
 * @param {string} page - Page name (home, chat, wiki, files, settings)
 * @param {string|null} sessionId - Optional chat session ID
 * @param {boolean} updateUrl - Whether to update browser URL (default: true)
 */
function navigateTo(page, sessionId = null, updateUrl = true) {
    // Update state
    state.currentPage = page;
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.dataset.page === page);
    });
    
    // Update pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.toggle('active', p.id === `page-${page}`);
    });
    
    // Update URL if needed
    if (updateUrl) {
        router.push(page, sessionId);
    }
    
    // Load page-specific content
    if (page === 'files') {
        loadFiles(state.currentPath);
    } else if (page === 'home') {
        loadStats();
    } else if (page === 'settings') {
        loadMcpServers();
        checkSystemStatus();
    } else if (page === 'chat') {
        checkChatStatus();
        // Handle chat session
        if (sessionId) {
            loadChatSession(sessionId);
        } else {
            // Check if we should create a new session or show existing
            showChatSessionSelector();
        }
    } else if (page === 'wiki') {
        loadWikiStructure();
    } else if (page === 'admin') {
        loadAdminPage();
    }
}

// Initialize navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.dataset.page;
        
        // Close mobile nav when a link is clicked
        closeMobileNav();
        
        // For chat, create new session; for others, just navigate
        if (page === 'chat') {
            navigateTo(page, null);
        } else {
            navigateTo(page);
        }
    });
});

// ═══════════════════════════════════════════════════════════════════════════
// Mobile Navigation
// ═══════════════════════════════════════════════════════════════════════════

function toggleMobileNav() {
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburger && navLinks) {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('mobile-open');
    }
}

function closeMobileNav() {
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburger && navLinks) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('mobile-open');
    }
}

// Close mobile nav when clicking outside
document.addEventListener('click', (e) => {
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (hamburger && navLinks && navLinks.classList.contains('mobile-open')) {
        if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
            closeMobileNav();
        }
    }
});

// ═══════════════════════════════════════════════════════════════════════════
// Wiki Sidebar Toggle (Mobile)
// ═══════════════════════════════════════════════════════════════════════════

function toggleWikiSidebar() {
    const sidebar = document.getElementById('wikiSidebar');
    const mobileBar = document.getElementById('wikiBreadcrumbMobile');
    
    if (sidebar) {
        sidebar.classList.toggle('mobile-open');
        if (mobileBar) {
            mobileBar.classList.toggle('open');
        }
    }
}

function closeWikiSidebar() {
    const sidebar = document.getElementById('wikiSidebar');
    const mobileBar = document.getElementById('wikiBreadcrumbMobile');
    
    if (sidebar) {
        sidebar.classList.remove('mobile-open');
        if (mobileBar) {
            mobileBar.classList.remove('open');
        }
    }
}

function updateWikiMobileBreadcrumb(text) {
    const mobileText = document.getElementById('wikiBreadcrumbMobileText');
    if (mobileText) {
        mobileText.textContent = text || 'Tap to browse tables';
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// MCP Connection & Health
// ═══════════════════════════════════════════════════════════════════════════

async function checkMcpHealth() {
    try {
        const response = await fetch('/api/mcp/health');
        const data = await response.json();
        
        const indicator = document.getElementById('mcpStatus');
        const text = document.getElementById('mcpStatusText');
        
        if (data.status === 'connected') {
            indicator.className = 'status-indicator connected';
            text.textContent = 'MCP Connected';
            state.mcpConnected = true;
        } else {
            indicator.className = 'status-indicator disconnected';
            text.textContent = 'MCP Disconnected';
            state.mcpConnected = false;
        }
    } catch (error) {
        const indicator = document.getElementById('mcpStatus');
        const text = document.getElementById('mcpStatusText');
        indicator.className = 'status-indicator disconnected';
        text.textContent = 'Connection Error';
        state.mcpConnected = false;
    }
}

async function loadStats() {
    try {
        // Load database stats
        const response = await fetch('/api/mcp/tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tool: 'list_databases', params: {} })
        });
        
        if (response.ok) {
            const data = await response.json();
            const databases = data.databases || data.content?.[0]?.text ? 
                JSON.parse(data.content[0].text).databases : [];
            
            // Update stats
            let totalTables = 0;
            databases.forEach(db => totalTables += db.table_count || 0);
            
            document.getElementById('stat-tables').textContent = totalTables || '--';
            document.getElementById('stat-databases').textContent = databases.length || '--';
        }
    } catch (error) {
        console.log('Could not load stats:', error);
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Chat Session Management
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate a unique session ID
 */
function generateSessionId() {
    return 'chat_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Load chat sessions from localStorage
 */
function loadChatSessionsFromStorage() {
    try {
        const stored = localStorage.getItem('chatSessions');
        if (stored) {
            state.chatSessions = JSON.parse(stored);
        }
    } catch (e) {
        console.error('Error loading chat sessions:', e);
        state.chatSessions = {};
    }
}

/**
 * Save chat sessions to localStorage
 */
function saveChatSessionsToStorage() {
    try {
        localStorage.setItem('chatSessions', JSON.stringify(state.chatSessions));
    } catch (e) {
        console.error('Error saving chat sessions:', e);
    }
}

/**
 * Create a new chat session
 */
function createNewChatSession() {
    const sessionId = generateSessionId();
    const session = {
        id: sessionId,
        title: 'New Chat',
        history: [],
        createdAt: new Date().toISOString()
    };
    
    state.chatSessions[sessionId] = session;
    state.currentSessionId = sessionId;
    state.chatHistory = [];
    
    saveChatSessionsToStorage();
    
    // Navigate to the new session URL
    router.push('chat', sessionId);
    
    // Clear chat UI (this also shows welcome message)
    clearChatUI();
    
    return sessionId;
}

/**
 * Load a specific chat session
 */
function loadChatSession(sessionId) {
    const session = state.chatSessions[sessionId];
    
    if (!session) {
        // Session doesn't exist, create a new one with this ID or redirect
        console.log(`Session ${sessionId} not found, creating new session`);
        const newSession = {
            id: sessionId,
            title: 'New Chat',
            history: [],
            createdAt: new Date().toISOString()
        };
        state.chatSessions[sessionId] = newSession;
        saveChatSessionsToStorage();
    }
    
    state.currentSessionId = sessionId;
    state.chatHistory = state.chatSessions[sessionId]?.history || [];
    
    // Render chat history
    renderChatHistory();
}

/**
 * Save current chat to session
 */
function saveCurrentChatSession() {
    if (!state.currentSessionId) return;
    
    const session = state.chatSessions[state.currentSessionId];
    if (session) {
        session.history = state.chatHistory;
        
        // Update title from first user message if it's still "New Chat"
        if (session.title === 'New Chat' && state.chatHistory.length > 0) {
            const firstUserMsg = state.chatHistory.find(m => m.role === 'user');
            if (firstUserMsg) {
                session.title = firstUserMsg.content.slice(0, 50) + (firstUserMsg.content.length > 50 ? '...' : '');
            }
        }
        
        saveChatSessionsToStorage();
    }
}

/**
 * Show chat session selector or create new session
 */
function showChatSessionSelector() {
    loadChatSessionsFromStorage();
    
    const sessions = Object.values(state.chatSessions).sort((a, b) => 
        new Date(b.createdAt) - new Date(a.createdAt)
    );
    
    if (sessions.length === 0) {
        // No sessions, create a new one
        createNewChatSession();
    } else {
        // Show existing chat or continue with current session
        if (state.currentSessionId && state.chatSessions[state.currentSessionId]) {
            loadChatSession(state.currentSessionId);
        } else {
            // Load most recent session
            createNewChatSession();
        }
    }
}

/**
 * Clear chat UI and restore welcome message
 */
function clearChatUI() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        // Re-insert the welcome message HTML
        chatMessages.innerHTML = `
            <div class="chat-welcome" id="chatWelcome">
                <div class="chat-welcome-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <rect x="2" y="3" width="20" height="14" rx="2"/>
                        <path d="M8 21h8M12 17v4"/>
                        <path d="M7 8h2M7 11h4"/>
                    </svg>
                </div>
                <h2 class="chat-welcome-title">Welcome to <span class="accent">CompanyMCP</span> Chat</h2>
                <p class="chat-welcome-text">
                    I'm your AI assistant with access to your database schemas and documentation. 
                    Ask me about tables, relationships, data models, or get help writing queries.
                </p>
                <div class="chat-welcome-features">
                    <div class="welcome-feature">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"/>
                            <path d="m21 21-4.35-4.35"/>
                        </svg>
                        <span>Search schemas</span>
                    </div>
                    <div class="welcome-feature">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                        </svg>
                        <span>Explore relationships</span>
                    </div>
                    <div class="welcome-feature">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="18" height="18" rx="2"/>
                            <path d="M3 9h18M9 21V9"/>
                        </svg>
                        <span>Generate SQL</span>
                    </div>
                </div>
            </div>
        `;
        // Show suggestions when chat is cleared
        showChatSuggestions();
    }
}

/**
 * Render chat history from loaded session
 */
function renderChatHistory() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    if (state.chatHistory.length === 0) {
        // Use clearChatUI which properly restores the welcome message
        clearChatUI();
        showChatSuggestions();
        return;
    }
    
    // Clear and render messages (no welcome message needed)
    chatMessages.innerHTML = '';
    hideChatSuggestions();
    
    // Render each message
    for (const msg of state.chatHistory) {
        addMessage(msg.role, msg.content);
    }
}

/**
 * Delete a chat session
 */
function deleteChatSession(sessionId) {
    delete state.chatSessions[sessionId];
    saveChatSessionsToStorage();
    
    // If deleting current session, create new one
    if (state.currentSessionId === sessionId) {
        createNewChatSession();
    }
}

/**
 * Get all chat sessions sorted by date
 */
function getAllChatSessions() {
    return Object.values(state.chatSessions).sort((a, b) => 
        new Date(b.createdAt) - new Date(a.createdAt)
    );
}

/**
 * Toggle sessions sidebar visibility
 */
function toggleSessionsList() {
    const sidebar = document.getElementById('chatSessionsSidebar');
    if (!sidebar) return;
    
    const isVisible = sidebar.classList.contains('visible');
    
    if (isVisible) {
        sidebar.classList.remove('visible');
    } else {
        sidebar.classList.add('visible');
        renderSessionsList();
    }
}

/**
 * Render the sessions list in the sidebar
 */
function renderSessionsList() {
    const sessionsList = document.getElementById('sessionsList');
    if (!sessionsList) return;
    
    const sessions = getAllChatSessions();
    
    if (sessions.length === 0) {
        sessionsList.innerHTML = '<div class="sessions-empty">No chat history yet</div>';
        return;
    }
    
    sessionsList.innerHTML = sessions.map(session => {
        const isActive = session.id === state.currentSessionId;
        const date = new Date(session.createdAt);
        const dateStr = formatSessionDate(date);
        
        return `
            <div class="session-item ${isActive ? 'active' : ''}" onclick="switchToSession('${session.id}')">
                <div class="session-info">
                    <div class="session-title">${escapeHtml(session.title)}</div>
                    <div class="session-date">${dateStr}</div>
                </div>
                <button class="session-delete" onclick="event.stopPropagation(); confirmDeleteSession('${session.id}')" title="Delete">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                        <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                </button>
            </div>
        `;
    }).join('');
}

/**
 * Format session date for display
 */
function formatSessionDate(date) {
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (days === 0) {
        return 'Today';
    } else if (days === 1) {
        return 'Yesterday';
    } else if (days < 7) {
        return `${days} days ago`;
    } else {
        return date.toLocaleDateString();
    }
}

/**
 * Switch to a different chat session
 */
function switchToSession(sessionId) {
    // Close sidebar
    const sidebar = document.getElementById('chatSessionsSidebar');
    if (sidebar) sidebar.classList.remove('visible');
    
    // Navigate to the session
    navigateTo('chat', sessionId);
}

/**
 * Confirm and delete a session
 */
function confirmDeleteSession(sessionId) {
    const session = state.chatSessions[sessionId];
    if (!session) return;
    
    if (confirm(`Delete "${session.title}"? This cannot be undone.`)) {
        deleteChatSession(sessionId);
        renderSessionsList();
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Chat Interface
// ═══════════════════════════════════════════════════════════════════════════

const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSend');
const chatMessages = document.getElementById('chatMessages');

// Auto-resize textarea
chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 200) + 'px';
});

// Send on Enter (without Shift)
chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

chatSend.addEventListener('click', sendMessage);

async function sendMessage(textOrEvent = null) {
    // Handle both direct calls with text and click events
    const text = (typeof textOrEvent === 'string') ? textOrEvent : null;
    const message = text || chatInput.value.trim();
    if (!message || state.isLoading) return;
    
    // Hide welcome message on first message
    hideWelcomeMessage();
    
    // Clear input
    if (!text) {
        chatInput.value = '';
        chatInput.style.height = 'auto';
    }
    
    // Add user message
    addMessage('user', message);
    
    // Show loading
    state.isLoading = true;
    chatSend.disabled = true;
    
    // Create streaming container
    const streamingContainer = createStreamingContainer();
    
    try {
        const response = await fetch('/api/chat/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message,
                history: state.chatHistory.slice(-10)
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        let buffer = '';
        let fullContent = '';
        let toolsUsed = [];
        let thinkingSteps = [];
        
        let chunkCount = 0;
        let currentEventType = null;
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                console.log(`[SSE] Stream ended after ${chunkCount} chunks`);
                break;
            }
            
            chunkCount++;
            const chunk = decoder.decode(value, { stream: true });
            console.log(`[SSE] Chunk ${chunkCount} received (${chunk.length} bytes)`);
            buffer += chunk;
            
            // Process complete SSE events (split by double newline)
            // SSE events are separated by \n\n
            const events = buffer.split('\n\n');
            buffer = events.pop() || ''; // Keep incomplete event in buffer
            
            for (const eventBlock of events) {
                if (!eventBlock.trim()) continue;
                
                const lines = eventBlock.split('\n');
                let eventType = null;
                let eventData = null;
                
                for (const line of lines) {
                    if (line.startsWith('event: ')) {
                        eventType = line.slice(7).trim();
                    } else if (line.startsWith('data: ')) {
                        eventData = line.slice(6);
                    }
                }
                
                if (eventType && eventData) {
                    try {
                        const data = JSON.parse(eventData);
                        console.log(`[SSE] Received ${eventType}:`, eventType === 'tool_result' ? '(tool result data)' : data);
                        handleStreamEvent(eventType, data, streamingContainer, {
                            thinkingSteps,
                            toolsUsed,
                            fullContent: () => fullContent,
                            setFullContent: (c) => { fullContent = c; }
                        });
                        
                        if (eventType === 'content_delta') {
                            fullContent += data.content;
                        } else if (eventType === 'tool_start' || eventType === 'tool_result') {
                            if (eventType === 'tool_result') {
                                thinkingSteps.push({
                                    type: 'tool_call',
                                    server: data.server,
                                    tool: data.tool,
                                    arguments: data.arguments,
                                    result: data.result
                                });
                                toolsUsed.push({
                                    server: data.server,
                                    tool: data.tool,
                                    arguments: data.arguments
                                });
                            }
                        } else if (eventType === 'thinking') {
                            thinkingSteps.push({
                                type: 'thinking',
                                content: data.content
                            });
                        } else if (eventType === 'content_done') {
                            fullContent = data.full_content || fullContent;
                            toolsUsed = data.tools_used || toolsUsed;
                        } else if (eventType === 'error') {
                            fullContent = `Error: ${data.message}`;
                        }
                    } catch (e) {
                        console.error(`[SSE] Error parsing ${eventType} data:`, e, eventData?.substring(0, 100));
                    }
                } else if (eventType) {
                    console.warn(`[SSE] Event ${eventType} has no data`);
                }
            }
        }
        
        // Finalize the streaming container
        finalizeStreamingContainer(streamingContainer, fullContent, toolsUsed);
        
        // Store in history
        state.chatHistory.push({ role: 'user', content: message });
        state.chatHistory.push({ role: 'assistant', content: fullContent });
        
        // Save to session storage
        saveCurrentChatSession();
        
    } catch (error) {
        console.error('Streaming error:', error);
        streamingContainer.remove();
        addMessage('assistant', `Sorry, I encountered an error: ${error.message}`, null, true);
    } finally {
        state.isLoading = false;
        chatSend.disabled = false;
    }
}

function createStreamingContainer() {
    const container = document.createElement('div');
    container.className = 'message assistant streaming';
    container.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="streaming-steps"></div>
            <div class="streaming-response">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(container);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return container;
}

function handleStreamEvent(eventType, data, container, state) {
    const stepsEl = container.querySelector('.streaming-steps');
    const responseEl = container.querySelector('.streaming-response');
    
    switch (eventType) {
        case 'thinking':
            addStreamingStep(stepsEl, 'thinking', {
                content: data.content
            });
            break;
            
        case 'tool_start':
            addStreamingStep(stepsEl, 'tool_start', {
                server: data.server,
                tool: data.tool,
                arguments: data.arguments
            });
            break;
            
        case 'tool_result':
            updateToolWithResult(stepsEl, data);
            break;
            
        case 'content_delta':
            // Remove typing indicator if present
            const typingIndicator = responseEl.querySelector('.typing-indicator');
            if (typingIndicator) {
                typingIndicator.remove();
            }
            
            // Append content
            let textEl = responseEl.querySelector('.message-text');
            if (!textEl) {
                textEl = document.createElement('div');
                textEl.className = 'message-text streaming-text';
                responseEl.appendChild(textEl);
            }
            
            // Update the full content and re-render
            const currentContent = state.fullContent() + data.content;
            textEl.innerHTML = parseContent(currentContent);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            break;
            
        case 'content_done':
            // Final content is handled in finalize
            break;
            
        case 'error':
            responseEl.innerHTML = `<div class="message-text error">${escapeHtml(data.message)}</div>`;
            break;
    }
}

function addStreamingStep(stepsEl, type, data) {
    // Ensure steps container is visible with collapsible details element
    if (!stepsEl.querySelector('.streaming-steps-details')) {
        const details = document.createElement('details');
        details.className = 'streaming-steps-details';
        details.open = true; // Keep open during streaming
        details.innerHTML = `
            <summary class="streaming-steps-header">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                <span>Agent Process</span>
                <span class="streaming-steps-status">Processing...</span>
                <svg class="streaming-steps-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path d="m6 9 6 6 6-6"/>
                </svg>
            </summary>
            <div class="streaming-steps-body"></div>
        `;
        stepsEl.appendChild(details);
    }
    
    const stepEl = document.createElement('div');
    stepEl.className = `streaming-step step-${type}`;
    
    if (type === 'thinking') {
        stepEl.innerHTML = `
            <div class="step-icon">💭</div>
            <div class="step-content">
                <div class="step-label">Thinking</div>
                <div class="step-text">${escapeHtml(data.content)}</div>
            </div>
        `;
    } else if (type === 'tool_start') {
        const isSQL = data.tool === 'execute_query' && data.arguments?.sql;
        const argsDisplay = isSQL 
            ? `<div class="step-sql"><pre><code class="language-sql">${escapeHtml(data.arguments.sql)}</code></pre></div>`
            : `<div class="step-args"><pre>${escapeHtml(JSON.stringify(data.arguments, null, 2))}</pre></div>`;
        
        stepEl.dataset.server = data.server;
        stepEl.dataset.tool = data.tool;
        stepEl.innerHTML = `
            <div class="step-icon">
                <div class="step-spinner"></div>
            </div>
            <div class="step-content">
                <div class="step-label">${escapeHtml(data.server)}/${escapeHtml(data.tool)}</div>
                ${argsDisplay}
                <div class="step-result-placeholder">
                    <span class="executing-text">Executing...</span>
                </div>
            </div>
        `;
    }
    
    // Append to the body inside the details element
    const stepsBody = stepsEl.querySelector('.streaming-steps-body');
    if (stepsBody) {
        stepsBody.appendChild(stepEl);
    } else {
        stepsEl.appendChild(stepEl);
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateToolWithResult(stepsEl, data) {
    // Find the matching tool step (look in the body container)
    const stepsBody = stepsEl.querySelector('.streaming-steps-body') || stepsEl;
    const steps = stepsBody.querySelectorAll('.streaming-step.step-tool_start');
    let targetStep = null;
    
    for (const step of steps) {
        if (step.dataset.server === data.server && step.dataset.tool === data.tool) {
            // Check if this step doesn't have a result yet
            if (step.querySelector('.step-result-placeholder')) {
                targetStep = step;
                break;
            }
        }
    }
    
    if (!targetStep) {
        // Create a new completed step if we can't find the pending one
        const stepEl = document.createElement('div');
        stepEl.className = 'streaming-step step-tool_result';
        
        const isSQL = data.tool === 'execute_query' && data.arguments?.sql;
        const argsDisplay = isSQL 
            ? `<div class="step-sql"><pre><code class="language-sql">${escapeHtml(data.arguments.sql)}</code></pre></div>`
            : `<div class="step-args"><pre>${escapeHtml(JSON.stringify(data.arguments, null, 2))}</pre></div>`;
        
        stepEl.innerHTML = `
            <div class="step-icon">🔧</div>
            <div class="step-content">
                <div class="step-label">${escapeHtml(data.server)}/${escapeHtml(data.tool)}</div>
                ${argsDisplay}
                <details class="step-result">
                    <summary>Result</summary>
                    <pre>${formatToolResult(data.result)}</pre>
                </details>
            </div>
        `;
        stepsBody.appendChild(stepEl);
    } else {
        // Update existing step
        targetStep.classList.remove('step-tool_start');
        targetStep.classList.add('step-tool_result');
        
        // Replace spinner with wrench icon
        const iconEl = targetStep.querySelector('.step-icon');
        if (iconEl) {
            iconEl.innerHTML = '🔧';
        }
        
        // Replace placeholder with result
        const placeholder = targetStep.querySelector('.step-result-placeholder');
        if (placeholder) {
            const resultEl = document.createElement('details');
            resultEl.className = 'step-result';
            resultEl.innerHTML = `
                <summary>Result</summary>
                <pre>${formatToolResult(data.result)}</pre>
            `;
            placeholder.replaceWith(resultEl);
        }
    }
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function finalizeStreamingContainer(container, fullContent, toolsUsed) {
    container.classList.remove('streaming');
    
    // Collapse the agent process details and update status
    const stepsDetails = container.querySelector('.streaming-steps-details');
    if (stepsDetails) {
        stepsDetails.open = false; // Collapse the details
        
        // Update status text
        const statusEl = stepsDetails.querySelector('.streaming-steps-status');
        if (statusEl) {
            const stepCount = stepsDetails.querySelectorAll('.streaming-step').length;
            statusEl.textContent = `${stepCount} step${stepCount !== 1 ? 's' : ''} completed`;
            statusEl.classList.add('completed');
        }
    }
    
    const responseEl = container.querySelector('.streaming-response');
    
    // Remove typing indicator if still present
    const typingIndicator = responseEl.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
    
    // Set final content
    let textEl = responseEl.querySelector('.message-text');
    if (!textEl) {
        textEl = document.createElement('div');
        textEl.className = 'message-text';
        responseEl.appendChild(textEl);
    }
    textEl.classList.remove('streaming-text');
    textEl.innerHTML = parseContent(fullContent);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(role, content, toolUsed = null, isError = false) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const avatar = role === 'assistant' ? 
        `<svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>` :
        `<svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>`;
    
    // Parse markdown-ish content
    const htmlContent = parseContent(content);
    
    messageEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text ${isError ? 'error' : ''}">${htmlContent}</div>
            ${toolUsed ? `<div class="message-tool">Used: ${toolUsed}</div>` : ''}
        </div>
    `;
    
    chatMessages.appendChild(messageEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addThinkingSteps(steps) {
    const stepsEl = document.createElement('div');
    stepsEl.className = 'message assistant thinking-steps';
    
    let stepsHtml = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="thinking-header">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                Agent Process
            </div>
            <div class="thinking-body">
    `;
    
    for (const step of steps) {
        if (step.type === 'thinking') {
            stepsHtml += `
                <div class="step step-thinking">
                    <div class="step-icon">💭</div>
                    <div class="step-content">
                        <div class="step-label">Thinking</div>
                        <div class="step-text">${escapeHtml(step.content)}</div>
                    </div>
                </div>
            `;
        } else if (step.type === 'tool_call') {
            const argsStr = JSON.stringify(step.arguments, null, 2);
            const resultStr = formatToolResult(step.result);
            const isSQL = step.tool === 'execute_query' && step.arguments.sql;
            
            stepsHtml += `
                <div class="step step-tool">
                    <div class="step-icon">🔧</div>
                    <div class="step-content">
                        <div class="step-label">${step.server}/${step.tool}</div>
                        ${isSQL ? `<div class="step-sql"><pre><code class="language-sql">${escapeHtml(step.arguments.sql)}</code></pre></div>` : 
                          `<div class="step-args"><pre>${escapeHtml(argsStr)}</pre></div>`}
                        <details class="step-result">
                            <summary>Result</summary>
                            <pre>${resultStr}</pre>
                        </details>
                    </div>
                </div>
            `;
        }
    }
    
    stepsHtml += `
            </div>
        </div>
    `;
    
    stepsEl.innerHTML = stepsHtml;
    chatMessages.appendChild(stepsEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatToolResult(result) {
    if (!result) return 'null';
    
    // Truncate large results
    const str = JSON.stringify(result, null, 2);
    if (str.length > 2000) {
        return escapeHtml(str.substring(0, 2000) + '\n... (truncated)');
    }
    return escapeHtml(str);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addLoadingIndicator() {
    const loadingEl = document.createElement('div');
    loadingEl.className = 'message assistant';
    loadingEl.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(loadingEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingEl;
}

function parseContent(content) {
    // Extract and parse tables first (before HTML escaping)
    const tables = [];
    const tableRegex = /\|(.+)\|\n\|[-:| ]+\|\n((?:\|.+\|\n?)+)/g;
    
    // Replace tables with placeholders
    let processed = content.replace(tableRegex, (match, headerRow, bodyRows) => {
        const headers = headerRow.split('|').map(h => h.trim()).filter(h => h);
        const rows = bodyRows.trim().split('\n').map(row => 
            row.split('|').map(cell => cell.trim()).filter(cell => cell)
        );
        
        let table = '<div class="chat-table-wrapper"><table class="chat-table"><thead><tr>';
        headers.forEach(h => {
            table += `<th>${escapeHtml(h)}</th>`;
        });
        table += '</tr></thead><tbody>';
        
        rows.forEach(row => {
            table += '<tr>';
            row.forEach((cell, idx) => {
                // Format numbers with commas for readability
                const formattedCell = formatTableCell(cell, idx);
                table += `<td>${formattedCell}</td>`;
            });
            table += '</tr>';
        });
        
        table += '</tbody></table></div>';
        tables.push(table);
        return `__TABLE_PLACEHOLDER_${tables.length - 1}__`;
    });
    
    // Now do normal markdown parsing with HTML escaping
    let html = processed
        // Escape HTML
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        // Headers
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Code blocks
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Lists
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Restore tables
    tables.forEach((table, idx) => {
        html = html.replace(`__TABLE_PLACEHOLDER_${idx}__`, table);
    });
    
    // Wrap in paragraphs
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    // Fix list items (wrap in ul)
    html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    
    return html;
}

function formatTableCell(cell, columnIndex) {
    // Check if it looks like a number (with optional commas and decimals)
    const numMatch = cell.match(/^-?[\d,]+\.?\d*$/);
    if (numMatch) {
        // Parse the number and format it nicely
        const num = parseFloat(cell.replace(/,/g, ''));
        if (!isNaN(num)) {
            // Format with commas and 2 decimal places for currency-like values
            if (cell.includes('.')) {
                return `<span class="table-number">${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>`;
            }
            return `<span class="table-number">${num.toLocaleString('en-US')}</span>`;
        }
    }
    return escapeHtml(cell);
}

// ═══════════════════════════════════════════════════════════════════════════
// File Browser
// ═══════════════════════════════════════════════════════════════════════════

async function loadFiles(path) {
    const filesList = document.getElementById('filesList');
    filesList.innerHTML = '<div class="loading">Loading files...</div>';
    
    try {
        const response = await fetch(`/api/files?path=${encodeURIComponent(path)}`);
        
        if (!response.ok) {
            throw new Error('Failed to load files');
        }
        
        const data = await response.json();
        state.currentPath = data.path;
        
        // Update breadcrumb
        updateBreadcrumb(data.path);
        
        // Render file list
        filesList.innerHTML = '';
        
        // Add parent directory link if not at root
        if (data.path !== '/data') {
            const parentEl = createFileItem({
                name: '..',
                path: data.parent,
                is_directory: true
            });
            filesList.appendChild(parentEl);
        }
        
        // Add files
        data.files.forEach(file => {
            const fileEl = createFileItem(file);
            filesList.appendChild(fileEl);
        });
        
        if (data.files.length === 0) {
            filesList.innerHTML = '<div class="loading">No files in this directory</div>';
        }
        
    } catch (error) {
        filesList.innerHTML = `<div class="loading">Error: ${error.message}</div>`;
    }
}

function createFileItem(file) {
    const el = document.createElement('div');
    el.className = `file-item ${file.is_directory ? 'directory' : ''}`;
    
    const icon = file.is_directory ?
        `<svg viewBox="0 0 24 24" fill="currentColor" class="file-icon">
            <path d="M10 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
        </svg>` :
        `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="file-icon">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
        </svg>`;
    
    const size = file.is_directory ? '' : formatSize(file.size);
    
    el.innerHTML = `
        ${icon}
        <span class="file-name">${escapeHtml(file.name)}</span>
        <span class="file-size">${size}</span>
    `;
    
    el.addEventListener('click', () => {
        if (file.is_directory) {
            loadFiles(file.path);
        } else {
            loadFilePreview(file.path);
            // Mark as active
            document.querySelectorAll('.file-item').forEach(f => f.classList.remove('active'));
            el.classList.add('active');
        }
    });
    
    return el;
}

function updateBreadcrumb(path) {
    const breadcrumb = document.getElementById('pathBreadcrumb');
    const parts = path.split('/').filter(Boolean);
    
    let html = '';
    let currentPath = '';
    
    parts.forEach((part, index) => {
        currentPath += '/' + part;
        const isLast = index === parts.length - 1;
        
        if (index > 0) {
            html += '<span class="breadcrumb-separator">/</span>';
        }
        
        html += `<span class="breadcrumb-item" data-path="${currentPath}" 
                  style="${isLast ? 'color: var(--accent-400)' : ''}">${part}</span>`;
    });
    
    breadcrumb.innerHTML = html;
    
    // Add click handlers
    breadcrumb.querySelectorAll('.breadcrumb-item').forEach(item => {
        item.addEventListener('click', () => loadFiles(item.dataset.path));
    });
}

async function loadFilePreview(path) {
    const previewHeader = document.getElementById('previewHeader');
    const previewContent = document.getElementById('previewContent');
    
    previewHeader.textContent = path.split('/').pop();
    previewContent.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const response = await fetch(`/api/files/content?path=${encodeURIComponent(path)}`);
        const data = await response.json();
        
        if (data.error) {
            previewContent.innerHTML = `<div class="preview-placeholder">
                <p>${data.error}</p>
                <p class="file-size">Size: ${formatSize(data.size)}</p>
            </div>`;
            return;
        }
        
        // Render content based on file type
        const ext = path.split('.').pop().toLowerCase();
        
        if (ext === 'json') {
            previewContent.innerHTML = `<pre class="preview-code preview-json">${syntaxHighlightJson(data.content)}</pre>`;
        } else if (ext === 'md' || ext === 'markdown') {
            // Render markdown with basic formatting
            previewContent.innerHTML = `<div class="preview-markdown">${renderMarkdown(data.content)}</div>`;
        } else {
            previewContent.innerHTML = `<pre class="preview-code">${escapeHtml(data.content)}</pre>`;
        }
        
    } catch (error) {
        previewContent.innerHTML = `<div class="preview-placeholder">
            <p>Error loading file: ${error.message}</p>
        </div>`;
    }
}

function syntaxHighlightJson(json) {
    try {
        // Try to pretty-print if it's valid JSON
        const obj = JSON.parse(json);
        json = JSON.stringify(obj, null, 2);
    } catch (e) {
        // Keep original if parse fails
    }
    
    return escapeHtml(json)
        .replace(/"([^"]+)":/g, '<span class="key">"$1"</span>:')
        .replace(/: "([^"]*)"([,\n])/g, ': <span class="string">"$1"</span>$2')
        .replace(/: (\d+)([,\n])/g, ': <span class="number">$1</span>$2')
        .replace(/: (true|false|null)([,\n])/g, ': <span class="number">$1</span>$2');
}


// ═══════════════════════════════════════════════════════════════════════════
// Wiki
// ═══════════════════════════════════════════════════════════════════════════

async function loadWikiStructure() {
    const wikiTree = document.getElementById('wikiTree');
    if (!wikiTree) return;
    
    // Only load if not already loaded
    if (state.wikiStructure) {
        renderWikiTree();
        return;
    }
    
    wikiTree.innerHTML = '<div class="loading">Loading databases...</div>';
    
    try {
        const response = await fetch('/api/wiki/structure');
        const data = await response.json();
        state.wikiStructure = data;
        renderWikiTree();
    } catch (error) {
        wikiTree.innerHTML = `<div class="loading">Error loading wiki: ${error.message}</div>`;
    }
}

function renderWikiTree() {
    const wikiTree = document.getElementById('wikiTree');
    if (!wikiTree || !state.wikiStructure) return;
    
    const databases = state.wikiStructure.databases || [];
    
    if (databases.length === 0) {
        wikiTree.innerHTML = '<div class="loading">No databases found</div>';
        return;
    }
    
    wikiTree.innerHTML = databases.map(db => renderDatabaseNode(db)).join('');
    
    // Add event listeners
    wikiTree.querySelectorAll('.wiki-node-header').forEach(header => {
        header.addEventListener('click', handleWikiNodeClick);
    });
}

function renderDatabaseNode(db) {
    const isExpanded = state.wikiExpandedNodes.has(`db:${db.name}`);
    const domainCount = db.domains?.length || 0;
    
    return `
        <div class="wiki-node database ${isExpanded ? 'expanded' : ''}" data-type="database" data-name="${escapeHtml(db.name)}">
            <div class="wiki-node-header">
                <span class="wiki-node-toggle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </span>
                <svg viewBox="0 0 24 24" fill="currentColor" class="wiki-node-icon database">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
                <span class="wiki-node-name">${escapeHtml(db.name)}</span>
                <span class="wiki-node-count">${domainCount} domain${domainCount !== 1 ? 's' : ''}</span>
            </div>
            <div class="wiki-node-children">
                ${(db.domains || []).map(domain => renderDomainNode(db.name, domain)).join('')}
            </div>
        </div>
    `;
}

function renderDomainNode(dbName, domain) {
    const nodeId = `domain:${dbName}/${domain.name}`;
    const isExpanded = state.wikiExpandedNodes.has(nodeId);
    const tableCount = domain.tables?.length || 0;
    
    return `
        <div class="wiki-node domain ${isExpanded ? 'expanded' : ''}" data-type="domain" data-db="${escapeHtml(dbName)}" data-name="${escapeHtml(domain.name)}">
            <div class="wiki-node-header">
                <span class="wiki-node-toggle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="wiki-node-icon domain">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                <span class="wiki-node-name">${escapeHtml(domain.name)}</span>
                <span class="wiki-node-count">${tableCount} table${tableCount !== 1 ? 's' : ''}</span>
            </div>
            <div class="wiki-node-children">
                ${(domain.tables || []).map(table => renderTableNode(dbName, domain.name, table)).join('')}
            </div>
        </div>
    `;
}

function renderTableNode(dbName, domainName, table) {
    const isSelected = state.wikiSelectedTable === table.path;
    
    return `
        <div class="wiki-node table" data-type="table" data-path="${escapeHtml(table.path)}">
            <div class="wiki-node-header ${isSelected ? 'active' : ''}">
                <span class="wiki-node-toggle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="wiki-node-icon table">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <path d="M3 9h18M9 21V9"/>
                </svg>
                <span class="wiki-node-name">${escapeHtml(table.name)}</span>
            </div>
        </div>
    `;
}

function handleWikiNodeClick(event) {
    const header = event.currentTarget;
    const node = header.closest('.wiki-node');
    const type = node.dataset.type;
    
    if (type === 'database') {
        const dbName = node.dataset.name;
        const nodeId = `db:${dbName}`;
        toggleWikiNode(nodeId, node);
    } else if (type === 'domain') {
        const dbName = node.dataset.db;
        const domainName = node.dataset.name;
        const nodeId = `domain:${dbName}/${domainName}`;
        toggleWikiNode(nodeId, node);
    } else if (type === 'table') {
        const path = node.dataset.path;
        loadWikiTable(path);
        
        // Update selected state
        document.querySelectorAll('.wiki-node.table .wiki-node-header').forEach(h => {
            h.classList.remove('active');
        });
        header.classList.add('active');
        state.wikiSelectedTable = path;
    }
}

function toggleWikiNode(nodeId, nodeElement) {
    if (state.wikiExpandedNodes.has(nodeId)) {
        state.wikiExpandedNodes.delete(nodeId);
        nodeElement.classList.remove('expanded');
    } else {
        state.wikiExpandedNodes.add(nodeId);
        nodeElement.classList.add('expanded');
    }
}

async function loadWikiTable(path) {
    const wikiDoc = document.getElementById('wikiDoc');
    const wikiBreadcrumb = document.getElementById('wikiBreadcrumb');
    
    if (!wikiDoc) return;
    
    wikiDoc.innerHTML = '<div class="loading">Loading documentation...</div>';
    
    // Close wiki sidebar on mobile when table is selected
    closeWikiSidebar();
    
    try {
        const response = await fetch(`/api/wiki/table?path=${encodeURIComponent(path)}`);
        
        if (!response.ok) {
            throw new Error('Failed to load table documentation');
        }
        
        const data = await response.json();
        
        // Update mobile breadcrumb text
        updateWikiMobileBreadcrumb(`${data.database} / ${data.domain} / ${data.name}`);
        
        // Update desktop breadcrumb
        if (wikiBreadcrumb) {
            wikiBreadcrumb.innerHTML = `
                <span class="breadcrumb-item" onclick="clearWikiSelection()">Wiki</span>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-item" onclick="expandWikiToDatabase('${escapeHtml(data.database)}')">${escapeHtml(data.database)}</span>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-item" onclick="expandWikiToDomain('${escapeHtml(data.database)}', '${escapeHtml(data.domain)}')">${escapeHtml(data.domain)}</span>
                <span class="breadcrumb-separator">/</span>
                <span class="breadcrumb-item current">${escapeHtml(data.name)}</span>
            `;
        }
        
        // Render markdown content
        const htmlContent = renderWikiMarkdown(data.content);
        wikiDoc.innerHTML = `<div class="wiki-doc-content">${htmlContent}</div>`;
        
    } catch (error) {
        wikiDoc.innerHTML = `<div class="wiki-placeholder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4M12 16h.01"/>
            </svg>
            <h3>Error Loading Documentation</h3>
            <p>${error.message}</p>
        </div>`;
    }
}

function renderWikiMarkdown(content) {
    // Enhanced markdown rendering for wiki pages
    let html = escapeHtml(content)
        // Headers
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.+?)__/g, '<strong>$1</strong>')
        // Code blocks
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Links
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // Handle tables
    html = renderMarkdownTables(html);
    
    // Lists
    html = html
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    
    // Line breaks
    html = html
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Wrap in paragraphs if needed
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    // Fix list items (wrap in ul)
    html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    
    return html;
}

function renderMarkdownTables(html) {
    // Match markdown tables
    const tableRegex = /\|(.+)\|\n\|[-:| ]+\|\n((?:\|.+\|\n?)+)/g;
    
    return html.replace(tableRegex, (match, headerRow, bodyRows) => {
        const headers = headerRow.split('|').map(h => h.trim()).filter(h => h);
        const rows = bodyRows.trim().split('\n').map(row => 
            row.split('|').map(cell => cell.trim()).filter(cell => cell)
        );
        
        let table = '<table><thead><tr>';
        headers.forEach(h => {
            table += `<th>${h}</th>`;
        });
        table += '</tr></thead><tbody>';
        
        rows.forEach(row => {
            table += '<tr>';
            row.forEach(cell => {
                table += `<td>${cell}</td>`;
            });
            table += '</tr>';
        });
        
        table += '</tbody></table>';
        return table;
    });
}

function clearWikiSelection() {
    state.wikiSelectedTable = null;
    document.querySelectorAll('.wiki-node.table .wiki-node-header').forEach(h => {
        h.classList.remove('active');
    });
    
    const wikiDoc = document.getElementById('wikiDoc');
    const wikiBreadcrumb = document.getElementById('wikiBreadcrumb');
    
    // Reset mobile breadcrumb text
    updateWikiMobileBreadcrumb('Tap to browse tables');
    
    if (wikiBreadcrumb) {
        wikiBreadcrumb.innerHTML = `<span class="breadcrumb-item">Select a table to view documentation</span>`;
    }
    
    if (wikiDoc) {
        wikiDoc.innerHTML = `
            <div class="wiki-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                    <path d="M8 7h8M8 11h8M8 15h5"/>
                </svg>
                <h3>Database Documentation Wiki</h3>
                <p>Browse databases, domains, and tables in the sidebar to view their documentation.</p>
            </div>
        `;
    }
}

function expandWikiToDatabase(dbName) {
    const nodeId = `db:${dbName}`;
    state.wikiExpandedNodes.add(nodeId);
    renderWikiTree();
}

function expandWikiToDomain(dbName, domainName) {
    state.wikiExpandedNodes.add(`db:${dbName}`);
    state.wikiExpandedNodes.add(`domain:${dbName}/${domainName}`);
    renderWikiTree();
}

// Wiki Search
const wikiSearchInput = document.getElementById('wikiSearch');
const wikiSearchClear = document.getElementById('wikiSearchClear');
let wikiSearchTimeout = null;

if (wikiSearchInput) {
    wikiSearchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        // Show/hide clear button
        if (wikiSearchClear) {
            wikiSearchClear.style.display = query ? 'flex' : 'none';
        }
        
        // Debounce search
        clearTimeout(wikiSearchTimeout);
        wikiSearchTimeout = setTimeout(() => {
            if (query.length >= 2) {
                searchWiki(query);
            } else if (query.length === 0) {
                showWikiTree();
            }
        }, 300);
    });
}

if (wikiSearchClear) {
    wikiSearchClear.addEventListener('click', () => {
        if (wikiSearchInput) {
            wikiSearchInput.value = '';
            wikiSearchClear.style.display = 'none';
            showWikiTree();
        }
    });
}

async function searchWiki(query) {
    const wikiTree = document.getElementById('wikiTree');
    const wikiSearchResults = document.getElementById('wikiSearchResults');
    
    if (!wikiSearchResults) return;
    
    // Hide tree, show results
    if (wikiTree) wikiTree.style.display = 'none';
    wikiSearchResults.style.display = 'block';
    wikiSearchResults.innerHTML = '<div class="loading">Searching...</div>';
    
    try {
        const response = await fetch(`/api/wiki/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        const results = data.results || [];
        
        if (results.length === 0) {
            wikiSearchResults.innerHTML = `
                <div class="wiki-search-no-results">
                    <p>No tables found matching "${escapeHtml(query)}"</p>
                </div>
            `;
            return;
        }
        
        wikiSearchResults.innerHTML = results.map(result => `
            <div class="wiki-search-result" onclick="selectWikiSearchResult('${escapeHtml(result.path)}')">
                <div class="wiki-search-result-name">${escapeHtml(result.name)}</div>
                <div class="wiki-search-result-path">${escapeHtml(result.database)} / ${escapeHtml(result.domain)}</div>
                ${result.snippet ? `<div class="wiki-search-result-snippet">${escapeHtml(result.snippet)}</div>` : ''}
            </div>
        `).join('');
        
    } catch (error) {
        wikiSearchResults.innerHTML = `<div class="wiki-search-no-results">Error: ${error.message}</div>`;
    }
}

function showWikiTree() {
    const wikiTree = document.getElementById('wikiTree');
    const wikiSearchResults = document.getElementById('wikiSearchResults');
    
    if (wikiTree) wikiTree.style.display = 'block';
    if (wikiSearchResults) wikiSearchResults.style.display = 'none';
}

function selectWikiSearchResult(path) {
    // Clear search
    if (wikiSearchInput) {
        wikiSearchInput.value = '';
    }
    if (wikiSearchClear) {
        wikiSearchClear.style.display = 'none';
    }
    showWikiTree();
    
    // Extract database and domain from path to expand tree
    const parts = path.split('/');
    if (parts.length >= 4) {
        const dbName = parts[0];
        const domainName = parts[2]; // skip "domains" folder
        expandWikiToDomain(dbName, domainName);
    }
    
    // Load the table
    loadWikiTable(path);
    state.wikiSelectedTable = path;
    
    // Update selection in tree after re-render
    setTimeout(() => {
        document.querySelectorAll('.wiki-node.table').forEach(node => {
            if (node.dataset.path === path) {
                node.querySelector('.wiki-node-header').classList.add('active');
            }
        });
    }, 100);
}

// ═══════════════════════════════════════════════════════════════════════════
// Utilities
// ═══════════════════════════════════════════════════════════════════════════

function formatSize(bytes) {
    if (!bytes) return '';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0;
    while (bytes >= 1024 && i < units.length - 1) {
        bytes /= 1024;
        i++;
    }
    return bytes.toFixed(i > 0 ? 1 : 0) + ' ' + units[i];
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderMarkdown(content) {
    // Basic markdown rendering
    let html = escapeHtml(content)
        // Headers
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.+?)__/g, '<strong>$1</strong>')
        // Code blocks
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Links
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        // Lists
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Wrap in paragraphs
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    // Fix list items (wrap in ul)
    html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    
    return html;
}

// ═══════════════════════════════════════════════════════════════════════════
// MCP Server Management
// ═══════════════════════════════════════════════════════════════════════════

async function loadMcpServers() {
    const serversList = document.getElementById('serversList');
    if (!serversList) return;
    
    serversList.innerHTML = '<div class="loading">Loading servers...</div>';
    
    try {
        // Check readonly mode first
        await checkAndApplySettingsReadonly();
        
        const response = await fetch('/api/mcp/servers');
        const data = await response.json();
        state.mcpServers = data.servers || {};
        
        renderServersList();
    } catch (error) {
        serversList.innerHTML = `<div class="loading">Error loading servers: ${error.message}</div>`;
    }
}

function renderServersList() {
    const serversList = document.getElementById('serversList');
    if (!serversList) return;
    
    const servers = Object.entries(state.mcpServers);
    
    if (servers.length === 0) {
        serversList.innerHTML = '<div class="loading">No servers configured</div>';
        return;
    }
    
    serversList.innerHTML = servers.map(([id, server]) => `
        <div class="server-item ${server.enabled ? '' : 'disabled'}" data-server-id="${id}">
            <div class="server-info">
                <div class="server-header">
                    <span class="server-name">${escapeHtml(server.name)}</span>
                    <span class="server-id">${escapeHtml(id)}</span>
                    ${id === 'default' ? '<span class="server-badge">Default</span>' : ''}
                </div>
                <div class="server-url">${escapeHtml(server.url)}</div>
                ${server.description ? `<div class="server-description">${escapeHtml(server.description)}</div>` : ''}
            </div>
            <div class="server-actions">
                <button class="btn-icon" onclick="checkServerHealth('${id}')" title="Check Health">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;">
                        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
                    </svg>
                </button>
                <button class="btn-icon" onclick="viewServerTools('${id}')" title="View Tools">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;">
                        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
                    </svg>
                </button>
                <label class="toggle" title="${server.enabled ? 'Disable' : 'Enable'} Server">
                    <input type="checkbox" ${server.enabled ? 'checked' : ''} onchange="toggleServer('${id}', this.checked)">
                    <span class="toggle-slider"></span>
                </label>
                ${id !== 'default' ? `
                    <button class="btn-icon btn-danger" onclick="deleteServer('${id}')" title="Delete Server">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;">
                            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        </svg>
                    </button>
                ` : ''}
            </div>
            <div class="server-status" id="status-${id}"></div>
        </div>
    `).join('');
    
    // Apply readonly mode to all server items if enabled
    if (settingsReadonlyMode) {
        const serverItems = serversList.querySelectorAll('.server-item');
        serverItems.forEach(item => applyServerItemReadonly(item));
    }
}

async function checkServerHealth(serverId) {
    const statusEl = document.getElementById(`status-${serverId}`);
    if (statusEl) {
        statusEl.innerHTML = '<span class="checking">Checking...</span>';
    }
    
    try {
        const response = await fetch(`/api/mcp/servers/${serverId}/health`);
        const data = await response.json();
        
        if (statusEl) {
            if (data.status === 'connected') {
                statusEl.innerHTML = '<span class="status-connected">✓ Connected</span>';
            } else {
                statusEl.innerHTML = `<span class="status-error">✗ ${data.error || 'Disconnected'}</span>`;
            }
        }
    } catch (error) {
        if (statusEl) {
            statusEl.innerHTML = `<span class="status-error">✗ ${error.message}</span>`;
        }
    }
}

async function viewServerTools(serverId) {
    const modal = document.getElementById('serverModal');
    const modalName = document.getElementById('modalServerName');
    const modalBody = document.getElementById('modalBody');
    
    modal.classList.add('active');
    modalName.textContent = state.mcpServers[serverId]?.name || serverId;
    modalBody.innerHTML = '<div class="loading">Loading tools...</div>';
    
    try {
        const response = await fetch(`/api/mcp/servers/${serverId}/tools`);
        const data = await response.json();
        
        if (data.error) {
            modalBody.innerHTML = `<div class="error-message">${data.error}</div>`;
            return;
        }
        
        const tools = data.tools || [];
        
        if (tools.length === 0) {
            modalBody.innerHTML = '<div class="empty-message">No tools available from this server.</div>';
            return;
        }
        
        modalBody.innerHTML = `
            <div class="tools-list">
                <p class="tools-count">${tools.length} tool${tools.length !== 1 ? 's' : ''} available</p>
                ${tools.map(tool => `
                    <div class="tool-item">
                        <div class="tool-name">${escapeHtml(tool.name)}</div>
                        <div class="tool-description">${escapeHtml(tool.description || 'No description')}</div>
                        ${tool.inputSchema?.properties ? `
                            <div class="tool-params">
                                <strong>Parameters:</strong>
                                ${Object.entries(tool.inputSchema.properties).map(([name, schema]) => 
                                    `<span class="param">${name}: ${schema.type || 'any'}</span>`
                                ).join('')}
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        modalBody.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    }
}

function closeServerModal() {
    const modal = document.getElementById('serverModal');
    modal.classList.remove('active');
}

async function toggleServer(serverId, enabled) {
    try {
        await fetch(`/api/mcp/servers/${serverId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enabled })
        });
        
        state.mcpServers[serverId].enabled = enabled;
        renderServersList();
    } catch (error) {
        alert(`Error toggling server: ${error.message}`);
        loadMcpServers();
    }
}

async function deleteServer(serverId) {
    if (!confirm(`Are you sure you want to delete the server "${state.mcpServers[serverId]?.name || serverId}"?`)) {
        return;
    }
    
    try {
        await fetch(`/api/mcp/servers/${serverId}`, {
            method: 'DELETE'
        });
        
        delete state.mcpServers[serverId];
        renderServersList();
    } catch (error) {
        alert(`Error deleting server: ${error.message}`);
    }
}

function refreshServers() {
    loadMcpServers();
    checkSystemStatus();
}

// Add Server Form Handler - defined once, attached in DOMContentLoaded

async function checkSystemStatus() {
    try {
        const response = await fetch('/api/chat/status');
        const data = await response.json();
        
        const openaiStatus = document.getElementById('openaiStatus');
        const mcpServersCount = document.getElementById('mcpServersCount');
        
        if (openaiStatus) {
            if (data.openai_configured) {
                openaiStatus.innerHTML = '<span class="status-dot connected"></span> Configured';
                state.openaiConfigured = true;
            } else {
                openaiStatus.innerHTML = '<span class="status-dot disconnected"></span> Not Configured';
                state.openaiConfigured = false;
            }
        }
        
        if (mcpServersCount) {
            mcpServersCount.textContent = `${data.enabled_servers} / ${data.mcp_servers_count}`;
        }
        
        // Count total tools
        let totalTools = 0;
        for (const [id, server] of Object.entries(state.mcpServers)) {
            if (server.enabled) {
                try {
                    const toolsResponse = await fetch(`/api/mcp/servers/${id}/tools`);
                    const toolsData = await toolsResponse.json();
                    totalTools += (toolsData.tools || []).length;
                } catch (e) {
                    // Ignore errors
                }
            }
        }
        
        const totalToolsCount = document.getElementById('totalToolsCount');
        if (totalToolsCount) {
            totalToolsCount.textContent = totalTools;
        }
        
    } catch (error) {
        console.error('Error checking system status:', error);
    }
}

async function checkChatStatus() {
    try {
        const response = await fetch('/api/chat/status');
        const data = await response.json();
        state.openaiConfigured = data.openai_configured || false;
    } catch (error) {
        state.openaiConfigured = false;
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Chat Welcome Message
// ═══════════════════════════════════════════════════════════════════════════

function hideWelcomeMessage() {
    const welcomeEl = document.getElementById('chatWelcome');
    if (welcomeEl && !welcomeEl.classList.contains('hidden')) {
        welcomeEl.classList.add('hidden');
    }
    // Also hide suggestions when chat has started
    hideChatSuggestions();
}

function showWelcomeMessage() {
    const welcomeEl = document.getElementById('chatWelcome');
    if (welcomeEl && state.chatHistory.length === 0) {
        welcomeEl.classList.remove('hidden');
        showChatSuggestions();
    }
}

function hideChatSuggestions() {
    const suggestions = document.querySelector('.chat-suggestions');
    if (suggestions) {
        suggestions.style.display = 'none';
    }
}

function showChatSuggestions() {
    const suggestions = document.querySelector('.chat-suggestions');
    if (suggestions && state.chatHistory.length === 0) {
        suggestions.style.display = 'flex';
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════
// Admin Page - Chat Cache Management
// ═══════════════════════════════════════════════════════════════════════════

// Admin state
const adminState = {
    cacheStatus: null,
    caches: [],
    recording: false,
    recordingTo: null,
};

async function loadAdminPage() {
    await refreshCacheStatus();
    await refreshCacheList();
    await loadSettingsReadonlyStatus();
}

async function refreshCacheStatus() {
    try {
        const response = await fetch('/api/admin/cache/status');
        const data = await response.json();
        adminState.cacheStatus = data;
        adminState.caches = data.cached_chats || [];
        adminState.recording = !!data.recording_to;
        adminState.recordingTo = data.recording_to;
        
        // Update Playback UI
        const enabledToggle = document.getElementById('cacheEnabled');
        const modeLabel = document.getElementById('cacheModeLabel');
        const activeSelect = document.getElementById('activeCacheSelect');
        const responseCacheSelect = document.getElementById('responseCache');
        
        if (enabledToggle) {
            enabledToggle.checked = data.enabled;
        }
        if (modeLabel) {
            modeLabel.textContent = data.enabled ? 'Enabled' : 'Disabled';
            modeLabel.className = data.enabled ? 'toggle-label enabled' : 'toggle-label';
        }
        
        // Populate playback cache select
        if (activeSelect) {
            activeSelect.innerHTML = '<option value="">-- Select Cache --</option>';
            for (const cache of adminState.caches) {
                activeSelect.innerHTML += `<option value="${cache.id}" ${cache.id === data.active_cache_id ? 'selected' : ''}>${escapeHtml(cache.title)} (${cache.response_count} responses)</option>`;
            }
        }
        
        // Populate recording cache select
        const recordingSelect = document.getElementById('recordingCacheSelect');
        if (recordingSelect) {
            recordingSelect.innerHTML = '<option value="">-- Not Recording --</option>';
            for (const cache of adminState.caches) {
                recordingSelect.innerHTML += `<option value="${cache.id}" ${cache.id === data.recording_to ? 'selected' : ''}>${escapeHtml(cache.title)} (${cache.response_count} responses)</option>`;
            }
        }
        
        // Update recording indicator
        const recordingIndicator = document.getElementById('recordingIndicator');
        const recordingLabel = document.getElementById('recordingLabel');
        
        if (data.recording_to) {
            const recordingCache = adminState.caches.find(c => c.id === data.recording_to);
            if (recordingIndicator) recordingIndicator.classList.add('active');
            if (recordingLabel) recordingLabel.textContent = `Recording to: ${recordingCache?.title || data.recording_to}`;
        } else {
            if (recordingIndicator) recordingIndicator.classList.remove('active');
            if (recordingLabel) recordingLabel.textContent = 'Not Recording';
        }
        
        // Legacy response cache select
        if (responseCacheSelect) {
            responseCacheSelect.innerHTML = '<option value="">-- Select Cache --</option>';
            for (const cache of adminState.caches) {
                responseCacheSelect.innerHTML += `<option value="${cache.id}">${escapeHtml(cache.title)}</option>`;
            }
        }
        
    } catch (error) {
        console.error('Error loading cache status:', error);
    }
}

async function toggleCacheMode(enabled) {
    try {
        // No need to select a cache - all caches are searched for matching prompts
        const response = await fetch(`/api/admin/cache/enable?enabled=${enabled}`, {
            method: 'POST',
        });
        
        if (!response.ok) {
            throw new Error('Failed to toggle cache mode');
        }
        
        await refreshCacheStatus();
    } catch (error) {
        alert(`Error: ${error.message}`);
        await refreshCacheStatus();
    }
}

async function setActiveCache(cacheId) {
    if (!cacheId) return;
    
    try {
        const enabledToggle = document.getElementById('cacheEnabled');
        const enabled = enabledToggle?.checked || false;
        
        if (enabled) {
            const response = await fetch(`/api/admin/cache/enable?enabled=true&cache_id=${cacheId}`, {
                method: 'POST',
            });
            
            if (!response.ok) {
                throw new Error('Failed to set active cache');
            }
        }
        
        await refreshCacheStatus();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function refreshCacheList() {
    const cachesList = document.getElementById('cachesList');
    if (!cachesList) return;
    
    try {
        const response = await fetch('/api/admin/cache/status');
        const data = await response.json();
        adminState.caches = data.cached_chats || [];
        
        if (adminState.caches.length === 0) {
            cachesList.innerHTML = '<div class="empty-message">No cached chats yet. Create one to get started.</div>';
            return;
        }
        
        cachesList.innerHTML = adminState.caches.map(cache => `
            <div class="cache-item" data-cache-id="${cache.id}">
                <div class="cache-info">
                    <div class="cache-header">
                        <span class="cache-title">${escapeHtml(cache.title)}</span>
                    </div>
                    <div class="cache-meta">
                        <span class="cache-responses">${cache.response_count} responses</span>
                        <span class="cache-plays" title="Total plays">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12">
                                <polygon points="5 3 19 12 5 21 5 3"/>
                            </svg>
                            ${cache.total_plays || 0} plays
                        </span>
                        <span class="cache-date">${cache.created_at ? new Date(cache.created_at).toLocaleDateString() : ''}</span>
                    </div>
                </div>
                <div class="cache-actions">
                    <button class="btn-icon" onclick="viewCacheDetails('${cache.id}')" title="View Details">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                    </button>
                    <button class="btn-icon" onclick="exportCache('${cache.id}')" title="Export cache">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                    </button>
                    <button class="btn-icon" onclick="startRecordingTo('${cache.id}')" title="Record to this cache">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                            <circle cx="12" cy="12" r="10"/>
                            <circle cx="12" cy="12" r="3" fill="currentColor"/>
                        </svg>
                    </button>
                    <button class="btn-icon btn-danger" onclick="deleteCache('${cache.id}')" title="Delete">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                            <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        </svg>
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        cachesList.innerHTML = `<div class="error-message">Error loading caches: ${error.message}</div>`;
    }
}

async function createCache(event) {
    event.preventDefault();
    
    const titleInput = document.getElementById('cacheTitleInput');
    const title = titleInput?.value.trim();
    
    if (!title) {
        alert('Please enter a cache title');
        return;
    }
    
    try {
        const response = await fetch('/api/admin/cache/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, messages: [] }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to create cache');
        }
        
        const data = await response.json();
        titleInput.value = '';
        
        await refreshCacheStatus();
        await refreshCacheList();
        
        alert(`Cache "${title}" created successfully!`);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function addCachedResponse(event) {
    event.preventDefault();
    
    const cacheSelect = document.getElementById('responseCache');
    const userMsgInput = document.getElementById('userMessageInput');
    const assistantInput = document.getElementById('assistantResponseInput');
    
    const cacheId = cacheSelect?.value;
    const userMessage = userMsgInput?.value.trim();
    const assistantResponse = assistantInput?.value.trim();
    
    if (!cacheId || !userMessage || !assistantResponse) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/cache/${cacheId}/add-response`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_message: userMessage,
                assistant_response: assistantResponse,
                tools_used: [],
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to add response');
        }
        
        userMsgInput.value = '';
        assistantInput.value = '';
        
        await refreshCacheList();
        
        alert('Response added successfully!');
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function deleteCache(cacheId) {
    const cache = adminState.caches.find(c => c.id === cacheId);
    if (!confirm(`Delete cache "${cache?.title || cacheId}"? This cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/cache/${cacheId}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete cache');
        }
        
        await refreshCacheStatus();
        await refreshCacheList();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function viewCacheDetails(cacheId) {
    try {
        const response = await fetch(`/api/admin/cache/${cacheId}`);
        const data = await response.json();
        
        // Show in modal
        const modal = document.getElementById('cacheModal');
        const title = document.getElementById('cacheModalTitle');
        const body = document.getElementById('cacheModalBody');
        
        if (!modal || !title || !body) {
            console.error('Cache modal elements not found');
            return;
        }
        
        title.textContent = data.title || 'Cache Details';
        
        if (!data.responses || data.responses.length === 0) {
            body.innerHTML = '<div class="empty-message">No cached responses yet.</div>';
        } else {
            const totalPlays = data.responses.reduce((sum, r) => sum + (r.play_count || 0), 0);
            body.innerHTML = `
                <div class="cache-detail-header">
                    <span class="cache-stat"><strong>${data.responses.length}</strong> responses</span>
                    <span class="cache-stat"><strong>${totalPlays}</strong> total plays</span>
                </div>
                <div class="cache-responses-list">
                    ${data.responses.map((r, i) => `
                        <div class="cache-response-card">
                            <div class="cache-response-header">
                                <span class="response-number">#${i + 1}</span>
                                <span class="play-count-badge" title="Times played">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                                        <polygon points="5 3 19 12 5 21 5 3"/>
                                    </svg>
                                    ${r.play_count || 0}
                                </span>
                            </div>
                            <div class="cache-response-section">
                                <label>Trigger Prompt:</label>
                                <div class="cache-prompt">${escapeHtml(r.user_message)}</div>
                            </div>
                            <div class="cache-response-section">
                                <label>Tool Calls (${(r.tools_used || []).length}):</label>
                                <div class="cache-tools">
                                    ${(r.tools_used || []).length === 0 ? '<em>No tool calls</em>' : 
                                        (r.tools_used || []).map(t => `
                                            <div class="tool-badge">
                                                <span class="tool-server">${t.server || 'unknown'}</span>
                                                <span class="tool-name">${t.tool}</span>
                                            </div>
                                        `).join('')
                                    }
                                </div>
                            </div>
                            <div class="cache-response-section">
                                <label>Response:</label>
                                <div class="cache-response-text">${escapeHtml(r.assistant_response).substring(0, 500)}${r.assistant_response.length > 500 ? '...' : ''}</div>
                            </div>
                            ${r.last_played ? `<div class="cache-response-footer">Last played: ${new Date(r.last_played).toLocaleString()}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        modal.classList.add('active');
    } catch (error) {
        alert(`Error loading cache details: ${error.message}`);
    }
}

function closeCacheModal() {
    const modal = document.getElementById('cacheModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

async function exportCache(cacheId) {
    try {
        // Trigger download via the export endpoint
        window.location.href = `/api/admin/cache/${cacheId}/export`;
    } catch (error) {
        alert(`Error exporting cache: ${error.message}`);
    }
}

async function importCache(file) {
    try {
        const text = await file.text();
        const cacheData = JSON.parse(text);
        
        const response = await fetch('/api/admin/cache/import', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cache_data: cacheData })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }
        
        const result = await response.json();
        alert(`Successfully imported "${result.title}" with ${result.response_count} responses!`);
        await refreshCacheList();
        await refreshCacheStatus();
    } catch (error) {
        alert(`Error importing cache: ${error.message}`);
    }
}

function triggerImportDialog() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            await importCache(file);
        }
    };
    input.click();
}

async function setRecordingCache(cacheId) {
    // Set or clear the recording cache
    try {
        if (cacheId) {
            const response = await fetch(`/api/admin/cache/${cacheId}/record`, { method: 'POST' });
            if (!response.ok) {
                throw new Error('Failed to start recording');
            }
            const cache = adminState.caches.find(c => c.id === cacheId);
            console.log(`[Admin] Started recording to: ${cache?.title || cacheId}`);
        } else {
            await fetch('/api/admin/cache/stop-recording', { method: 'POST' });
            console.log('[Admin] Stopped recording');
        }
        await refreshCacheStatus();
    } catch (error) {
        alert(`Error: ${error.message}`);
        await refreshCacheStatus();
    }
}

async function toggleRecording() {
    // Legacy function - use the dropdown instead
    const recordingSelect = document.getElementById('recordingCacheSelect');
    if (adminState.recording) {
        // Stop recording
        if (recordingSelect) recordingSelect.value = '';
        await setRecordingCache(null);
    } else {
        // Can't start without selecting a cache
        alert('Please select a cache from the dropdown to start recording');
    }
}

async function startRecordingTo(cacheId) {
    try {
        const response = await fetch(`/api/admin/cache/${cacheId}/record`, { method: 'POST' });
        
        if (!response.ok) {
            throw new Error('Failed to start recording');
        }
        
        adminState.recording = true;
        adminState.recordingTo = cacheId;
        
        const recordingIndicator = document.getElementById('recordingIndicator');
        const recordBtn = document.getElementById('recordBtn');
        const recordingLabel = document.getElementById('recordingLabel');
        
        const cache = adminState.caches.find(c => c.id === cacheId);
        
        if (recordingIndicator) recordingIndicator.classList.add('active');
        if (recordingLabel) recordingLabel.textContent = `Recording to: ${cache?.title || cacheId}`;
        if (recordBtn) recordBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14">
                <rect x="6" y="6" width="12" height="12"/>
            </svg>
            Stop
        `;
        
        alert(`Recording mode started. Chat responses will be saved to "${cache?.title || cacheId}"`);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}


// ═══════════════════════════════════════════════════════════════════════════
// Settings Page Lock (Admin)
// ═══════════════════════════════════════════════════════════════════════════

let settingsReadonlyMode = false;

async function loadSettingsReadonlyStatus() {
    try {
        const response = await fetch('/api/admin/settings');
        const data = await response.json();
        settingsReadonlyMode = data.settings_readonly || false;
        
        // Update admin toggle if on admin page
        const toggle = document.getElementById('settingsReadonly');
        const label = document.getElementById('settingsReadonlyLabel');
        if (toggle) {
            toggle.checked = settingsReadonlyMode;
        }
        if (label) {
            label.textContent = settingsReadonlyMode ? 'Locked' : 'Unlocked';
            label.className = settingsReadonlyMode ? 'toggle-label enabled' : 'toggle-label';
        }
        
        return settingsReadonlyMode;
    } catch (error) {
        console.error('Error loading settings readonly status:', error);
        return false;
    }
}

async function toggleSettingsReadonly(enabled) {
    try {
        const response = await fetch(`/api/admin/settings/readonly?enabled=${enabled}`, {
            method: 'POST',
        });
        
        if (!response.ok) {
            throw new Error('Failed to toggle settings readonly mode');
        }
        
        settingsReadonlyMode = enabled;
        
        // Update label
        const label = document.getElementById('settingsReadonlyLabel');
        if (label) {
            label.textContent = enabled ? 'Locked' : 'Unlocked';
            label.className = enabled ? 'toggle-label enabled' : 'toggle-label';
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
        // Revert toggle
        const toggle = document.getElementById('settingsReadonly');
        if (toggle) toggle.checked = !enabled;
    }
}

async function checkAndApplySettingsReadonly() {
    try {
        const response = await fetch('/api/settings/readonly');
        const data = await response.json();
        settingsReadonlyMode = data.readonly || false;
        
        if (settingsReadonlyMode) {
            applySettingsReadonlyMode();
        }
    } catch (error) {
        console.error('Error checking settings readonly mode:', error);
    }
}

function applySettingsReadonlyMode() {
    // Disable Add Server button
    const addServerBtn = document.querySelector('#addServerForm button[type="submit"]');
    if (addServerBtn) {
        addServerBtn.disabled = true;
        addServerBtn.title = 'Settings are locked by administrator';
        addServerBtn.style.opacity = '0.5';
        addServerBtn.style.cursor = 'not-allowed';
    }
    
    // Disable all form inputs in add server form
    const addServerForm = document.getElementById('addServerForm');
    if (addServerForm) {
        const inputs = addServerForm.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.disabled = true;
        });
    }
    
    // Add a notice banner
    const settingsHeader = document.querySelector('.settings-header');
    if (settingsHeader && !document.getElementById('readonlyBanner')) {
        const banner = document.createElement('div');
        banner.id = 'readonlyBanner';
        banner.className = 'readonly-banner';
        banner.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <span>Settings are locked in read-only mode</span>
        `;
        settingsHeader.appendChild(banner);
    }
}

function applyServerItemReadonly(serverItem) {
    if (!settingsReadonlyMode) return;
    
    // Disable toggle switches (keep them in enabled position)
    const toggleInput = serverItem.querySelector('.toggle input');
    if (toggleInput) {
        toggleInput.checked = true; // Force enabled
        toggleInput.disabled = true;
    }
    
    // Disable delete button
    const deleteBtn = serverItem.querySelector('.btn-danger');
    if (deleteBtn) {
        deleteBtn.disabled = true;
        deleteBtn.style.opacity = '0.3';
        deleteBtn.style.cursor = 'not-allowed';
        deleteBtn.onclick = null;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Load chat sessions from storage
    loadChatSessionsFromStorage();
    
    // Initialize router (handles initial URL navigation)
    router.init();
    
    // Check MCP health
    checkMcpHealth();
    setInterval(checkMcpHealth, 30000); // Check every 30 seconds
    
    // Initialize form handler for add server
    const addServerForm = document.getElementById('addServerForm');
    if (addServerForm) {
        addServerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const serverId = document.getElementById('serverId').value.trim().toLowerCase();
            const serverName = document.getElementById('serverName').value.trim();
            const serverUrl = document.getElementById('serverUrl').value.trim();
            const serverDescription = document.getElementById('serverDescription').value.trim();
            
            try {
                const response = await fetch(`/api/mcp/servers/${serverId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: serverName,
                        url: serverUrl,
                        enabled: true,
                        description: serverDescription
                    })
                });
                
                if (!response.ok) {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to add server');
                }
                
                // Clear form
                addServerForm.reset();
                
                // Reload servers
                loadMcpServers();
                checkSystemStatus();
                
            } catch (error) {
                alert(`Error adding server: ${error.message}`);
            }
        });
    }
});


// ═══════════════════════════════════════════════════════════════════════════
// Email Capture
// ═══════════════════════════════════════════════════════════════════════════

async function submitEmailCapture(event) {
    event.preventDefault();
    
    const emailInput = document.getElementById('emailCaptureInput');
    const submitBtn = document.getElementById('emailSubmitBtn');
    const statusEl = document.getElementById('emailCaptureStatus');
    
    const email = emailInput.value.trim();
    
    if (!email) {
        showEmailStatus('Please enter your email address', 'error');
        return;
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showEmailStatus('Please enter a valid email address', 'error');
        return;
    }
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    statusEl.textContent = '';
    statusEl.className = 'email-capture-status';
    
    try {
        const response = await fetch('/api/email/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showEmailStatus(data.message || 'Successfully subscribed!', 'success');
            emailInput.value = '';
        } else {
            showEmailStatus(data.detail || 'Something went wrong. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Email capture error:', error);
        showEmailStatus('Network error. Please try again later.', 'error');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

function showEmailStatus(message, type) {
    const statusEl = document.getElementById('emailCaptureStatus');
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.className = `email-capture-status ${type}`;
        
        // Clear success message after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                statusEl.textContent = '';
                statusEl.className = 'email-capture-status';
            }, 5000);
        }
    }
}




