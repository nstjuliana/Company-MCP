/**
 * Company MCP Frontend - JavaScript Application
 * Handles navigation, chat, and file browsing
 */

// ═══════════════════════════════════════════════════════════════════════════
// State Management
// ═══════════════════════════════════════════════════════════════════════════

const state = {
    currentPage: 'home',
    mcpConnected: false,
    chatHistory: [],
    currentPath: '/data',
    isLoading: false
};

// ═══════════════════════════════════════════════════════════════════════════
// Navigation
// ═══════════════════════════════════════════════════════════════════════════

function navigateTo(page) {
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
    
    // Load page-specific content
    if (page === 'files') {
        loadFiles(state.currentPath);
    } else if (page === 'home') {
        loadStats();
    }
}

// Initialize navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(link.dataset.page);
    });
});

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

async function sendMessage(text = null) {
    const message = text || chatInput.value.trim();
    if (!message || state.isLoading) return;
    
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
    const loadingEl = addLoadingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message,
                history: state.chatHistory.slice(-10) // Last 10 messages for context
            })
        });
        
        const data = await response.json();
        
        // Remove loading
        loadingEl.remove();
        
        // Add assistant response
        addMessage('assistant', data.response, data.tool_used);
        
        // Store in history
        state.chatHistory.push({ role: 'user', content: message });
        state.chatHistory.push({ role: 'assistant', content: data.response });
        
    } catch (error) {
        loadingEl.remove();
        addMessage('assistant', `Sorry, I encountered an error: ${error.message}`, null, true);
    } finally {
        state.isLoading = false;
        chatSend.disabled = false;
    }
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
    // Simple markdown-ish parsing
    let html = content
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
    
    // Wrap in paragraphs
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    // Fix list items (wrap in ul)
    html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    
    return html;
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

// ═══════════════════════════════════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Check MCP health
    checkMcpHealth();
    setInterval(checkMcpHealth, 30000); // Check every 30 seconds
    
    // Load initial stats
    loadStats();
});

