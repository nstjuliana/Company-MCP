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
    openaiConfigured: false
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
    } else if (page === 'settings') {
        loadMcpServers();
        checkSystemStatus();
    } else if (page === 'chat') {
        checkChatStatus();
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
        
        // Format tools used info
        let toolsInfo = null;
        if (data.tools_used && data.tools_used.length > 0) {
            toolsInfo = data.tools_used.map(t => `${t.server}/${t.tool}`).join(', ');
        } else if (data.tool_used) {
            toolsInfo = data.tool_used;
        }
        
        // Add assistant response
        addMessage('assistant', data.response, toolsInfo, data.error);
        
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
// MCP Server Management
// ═══════════════════════════════════════════════════════════════════════════

async function loadMcpServers() {
    const serversList = document.getElementById('serversList');
    if (!serversList) return;
    
    serversList.innerHTML = '<div class="loading">Loading servers...</div>';
    
    try {
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

// Add Server Form Handler
document.getElementById('addServerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const serverId = document.getElementById('serverId').value.trim();
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
        e.target.reset();
        
        // Reload servers
        loadMcpServers();
        checkSystemStatus();
        
    } catch (error) {
        alert(`Error adding server: ${error.message}`);
    }
});

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
    const statusDot = document.getElementById('chatStatusDot');
    const statusText = document.getElementById('chatStatusText');
    
    if (!statusDot || !statusText) return;
    
    try {
        const response = await fetch('/api/chat/status');
        const data = await response.json();
        
        if (data.openai_configured) {
            statusDot.className = 'status-dot connected';
            statusText.textContent = `GPT-4o Ready • ${data.enabled_servers} MCP server${data.enabled_servers !== 1 ? 's' : ''} connected`;
            state.openaiConfigured = true;
        } else {
            statusDot.className = 'status-dot disconnected';
            statusText.textContent = 'OpenAI API not configured';
            state.openaiConfigured = false;
        }
    } catch (error) {
        statusDot.className = 'status-dot disconnected';
        statusText.textContent = 'Error checking status';
    }
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
    
    // Check chat status
    checkChatStatus();
    
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



