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
    wikiSearchQuery: ''
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
    } else if (page === 'wiki') {
        loadWikiStructure();
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

async function findAllMarkdownFiles() {
    const filesList = document.getElementById('filesList');
    const findBtn = document.getElementById('findMarkdownBtn');
    
    // Disable button and show loading
    findBtn.disabled = true;
    findBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;margin-right:8px;"><path d="M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"/></svg> Searching...';
    filesList.innerHTML = '<div class="loading">Searching for markdown files...</div>';
    
    try {
        const response = await fetch('/api/files/markdown');
        
        if (!response.ok) {
            throw new Error('Failed to find markdown files');
        }
        
        const data = await response.json();
        
        // Update breadcrumb to show we're in search results
        const breadcrumb = document.getElementById('pathBreadcrumb');
        breadcrumb.innerHTML = `<span class="breadcrumb-item" data-path="/data" style="color: var(--accent-400);">Markdown Files (${data.count})</span>`;
        
        // Clear breadcrumb click handlers since we're in search mode
        breadcrumb.querySelectorAll('.breadcrumb-item').forEach(item => {
            item.addEventListener('click', () => {
                loadFiles('/data');
                findBtn.disabled = false;
                findBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;margin-right:8px;"><path d="M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"/></svg> Find All Markdown Files';
            });
        });
        
        // Render markdown files list
        filesList.innerHTML = '';
        
        if (data.files.length === 0) {
            filesList.innerHTML = '<div class="loading">No markdown files found</div>';
        } else {
            data.files.forEach(file => {
                const fileEl = createMarkdownFileItem(file);
                filesList.appendChild(fileEl);
            });
        }
        
    } catch (error) {
        filesList.innerHTML = `<div class="loading">Error: ${error.message}</div>`;
    } finally {
        findBtn.disabled = false;
        findBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;min-width:16px;min-height:16px;flex-shrink:0;margin-right:8px;"><path d="M21 21l-6-6m2-5a7 7 0 1 1-14 0 7 7 0 0 1 14 0z"/></svg> Find All Markdown Files';
    }
}

function createMarkdownFileItem(file) {
    const el = document.createElement('div');
    el.className = 'file-item';
    
    const icon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="file-icon">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
    </svg>`;
    
    const size = formatSize(file.size);
    const pathParts = file.relative_path.split('/');
    const displayPath = pathParts.length > 1 ? pathParts.slice(0, -1).join('/') + '/' : '';
    
    el.innerHTML = `
        ${icon}
        <div class="file-info">
            <span class="file-name">${escapeHtml(file.name)}</span>
            <span class="file-path">${escapeHtml(displayPath)}</span>
        </div>
        <span class="file-size">${size}</span>
    `;
    
    el.addEventListener('click', () => {
        loadFilePreview(file.path);
        // Mark as active
        document.querySelectorAll('.file-item').forEach(f => f.classList.remove('active'));
        el.classList.add('active');
    });
    
    return el;
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
    
    try {
        const response = await fetch(`/api/wiki/table?path=${encodeURIComponent(path)}`);
        
        if (!response.ok) {
            throw new Error('Failed to load table documentation');
        }
        
        const data = await response.json();
        
        // Update breadcrumb
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
    
    if (wikiBreadcrumb) {
        wikiBreadcrumb.innerHTML = '<span class="breadcrumb-item">Select a table to view documentation</span>';
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



