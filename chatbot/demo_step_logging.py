"""
Demo version of the chatbot web app with step logging UI.
This simplified version shows the step logging functionality without MCP dependencies.
"""

import os
import json
import uuid
from flask import Flask, render_template_string, request, jsonify, session, Response
from flask_cors import CORS
import time
import queue
import threading

app = Flask(__name__)
app.secret_key = "demo-secret-key"
CORS(app, supports_credentials=True)

# Global queue for step updates (session_id -> queue)
step_queues = {}
step_queues_lock = threading.Lock()

def send_step_update(session_id: str, step: str, status: str = "in_progress"):
    """Send a step update to the client's SSE queue."""
    with step_queues_lock:
        if session_id in step_queues:
            try:
                step_queues[session_id].put({
                    "step": step,
                    "status": status,
                    "timestamp": time.time()
                }, timeout=1)
            except:
                pass

def cleanup_old_queues():
    """Clean up old SSE queues periodically."""
    with step_queues_lock:
        current_time = time.time()
        to_remove = []
        for session_id, q in step_queues.items():
            try:
                if hasattr(q, '_last_activity') and current_time - q._last_activity > 1800:
                    to_remove.append(session_id)
            except:
                pass
        for session_id in to_remove:
            del step_queues[session_id]

def simulate_ai_processing(session_id: str):
    """Simulate AI processing with step updates."""
    steps = [
        ("Analyzing your question...", 1),
        ("Calling Answer Question tool...", 2),
        ("Generating SQL query...", 1),
        ("Executing database query...", 3),
        ("Processing results...", 1),
        ("Formatting response...", 1),
    ]

    for step, delay in steps:
        send_step_update(session_id, step)
        time.sleep(delay)

    send_step_update(session_id, "Response ready", "completed")

@app.route('/steps/<session_id>')
def step_updates(session_id):
    """Server-Sent Events endpoint for step updates."""
    def generate():
        # Create queue for this session if it doesn't exist
        with step_queues_lock:
            if session_id not in step_queues:
                step_queues[session_id] = queue.Queue(maxsize=50)

        q = step_queues[session_id]

        while True:
            try:
                # Wait for updates with timeout
                update = q.get(timeout=30)
                q._last_activity = time.time()

                # Send the update
                yield f"data: {json.dumps(update)}\n\n"

            except queue.Empty:
                # Send heartbeat to keep connection alive
                yield f"data: {json.dumps({'heartbeat': True})}\n\n"
            except Exception as e:
                break

    return Response(generate(), mimetype='text/event-stream')

# HTML template with step logging UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Step Logging Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: #4285f4;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-title {
            color: white;
            font-size: 1rem;
            font-weight: 500;
        }

        .status-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            backdrop-filter: blur(2px);
        }

        .status-overlay.visible {
            display: flex;
        }

        .status-bar {
            background: white;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            font-size: 1rem;
            color: #333;
            display: flex;
            align-items: center;
            gap: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            min-width: 300px;
            text-align: center;
        }

        .status-spinner {
            width: 16px;
            height: 16px;
            border: 2px solid #e9ecef;
            border-radius: 50%;
            border-top-color: #4285f4;
            animation: spin 0.8s linear infinite;
        }

        .status-text {
            flex: 1;
            font-weight: 500;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 600px;
            margin: 0 auto;
            width: 100%;
            background: white;
            box-shadow: 0 0 1px rgba(0, 0, 0, 0.1);
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .message-wrapper {
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
        }

        .message-wrapper.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .avatar.bot {
            background: #e8eaf6;
        }

        .avatar.user {
            background: #e3f2fd;
        }

        .avatar svg {
            width: 20px;
            height: 20px;
        }

        .message {
            max-width: 70%;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            position: relative;
        }

        .message.bot {
            background: #f5f5f5;
            color: #333;
            border-bottom-left-radius: 4px;
        }

        .message.user {
            background: #4285f4;
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message-content {
            margin-bottom: 0.25rem;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .message-timestamp {
            font-size: 0.75rem;
            opacity: 0.6;
            margin-top: 0.25rem;
        }

        .input-container {
            padding: 1rem;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 0.5rem;
            align-items: center;
            position: sticky;
            bottom: 0;
            background: white;
            z-index: 90;
        }

        .input-wrapper {
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
        }

        #message-input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            font-size: 0.9rem;
            font-family: inherit;
            outline: none;
            resize: none;
            min-height: 40px;
            max-height: 120px;
        }

        #message-input:focus {
            border-color: #4285f4;
        }

        .send-button {
            width: 36px;
            height: 36px;
            border: none;
            background: #4285f4;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        .send-button:hover:not(:disabled) {
            background: #357ae8;
        }

        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .send-button svg {
            width: 18px;
            height: 18px;
            color: white;
        }

        .loading {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
        }

        @media (max-width: 768px) {
            .container {
                max-width: 100%;
            }
            .message {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">Chatbot Step Logging Demo</div>
    </div>

    <div class="status-overlay" id="status-overlay">
        <div class="status-bar" id="status-bar">
            <div class="status-spinner"></div>
            <div class="status-text" id="status-text">Initializing...</div>
        </div>
    </div>

    <div class="container">

        <div class="chat-messages" id="chat-messages">
            <div class="message-wrapper bot">
                <div class="avatar bot">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                        <circle cx="9" cy="9" r="1.5"></circle>
                        <circle cx="15" cy="9" r="1.5"></circle>
                        <path d="M9 15h6"></path>
                    </svg>
                </div>
                <div class="message bot">
                    <div class="message-content">
                        Hi! This demo shows the step logging feature. Ask me a question to see the real-time progress updates!
                    </div>
                    <div class="message-timestamp" id="welcome-timestamp"></div>
                </div>
            </div>
        </div>

        <div class="input-container">
            <div class="input-wrapper">
                <input
                    type="text"
                    id="message-input"
                    placeholder="Type a message to see step logging..."
                    onkeydown="handleKeyPress(event)"
                />
            </div>
            <button class="send-button" id="send-button" onclick="sendMessage()" type="button">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
            </button>
        </div>
    </div>

    <script>
        let isLoading = false;
        let currentSessionId = null;
        let eventSource = null;
        const chatMessages = document.getElementById('chat-messages');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const statusOverlay = document.getElementById('status-overlay');
        const statusText = document.getElementById('status-text');

        // Set welcome message timestamp
        document.getElementById('welcome-timestamp').textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function connectSSE(sessionId) {
            if (eventSource) {
                eventSource.close();
            }
            currentSessionId = sessionId;
            eventSource = new EventSource(`/steps/${sessionId}`);

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.step) {
                    updateStatus(data.step, data.status);
                }
            };

            eventSource.onerror = function(event) {
                console.log('SSE connection error:', event);
            };
        }

        function updateStatus(step, status = 'in_progress') {
            statusText.textContent = step;
            statusOverlay.classList.add('visible');

            if (status === 'completed') {
                setTimeout(() => {
                    statusOverlay.classList.remove('visible');
                }, 2000);
            }
        }

        function disconnectSSE() {
            if (eventSource) {
                eventSource.close();
                eventSource = null;
            }
            statusOverlay.classList.remove('visible');
        }

        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message || isLoading) return;

            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.focus();

            isLoading = true;
            sendButton.disabled = true;
            sendToBackend(message);
        }

        function addMessage(content, type) {
            const wrapper = document.createElement('div');
            wrapper.className = `message-wrapper ${type}`;

            const avatar = document.createElement('div');
            avatar.className = `avatar ${type}`;

            if (type === 'bot') {
                avatar.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                        <circle cx="9" cy="9" r="1.5"></circle>
                        <circle cx="15" cy="9" r="1.5"></circle>
                        <path d="M9 15h6"></path>
                    </svg>
                `;
            } else {
                avatar.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="none" stroke="#4285f4" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                `;
            }

            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = content.replace(/\\n/g, '<br>');

            const timestampDiv = document.createElement('div');
            timestampDiv.className = 'message-timestamp';
            timestampDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(timestampDiv);

            wrapper.appendChild(avatar);
            wrapper.appendChild(messageDiv);

            chatMessages.appendChild(wrapper);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        async function sendToBackend(message) {
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                // Connect to SSE for step updates
                if (data.session_id && data.session_id !== currentSessionId) {
                    connectSSE(data.session_id);
                }

                if (data.response) {
                    addMessage(data.response, 'bot');
                } else {
                    addMessage('Sorry, I couldn\\'t process your request.', 'bot');
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, there was an error connecting to the server.', 'bot');
            } finally {
                isLoading = false;
                sendButton.disabled = false;
                setTimeout(() => {
                    if (!isLoading) {
                        statusOverlay.classList.remove('visible');
                        disconnectSSE();
                    }
                }, 1000);
            }
        }

        // Focus input on load
        window.addEventListener('load', () => {
            messageInput.focus();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the demo chatbot interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages with simulated step logging.
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing message parameter"}), 400

        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Empty message"}), 400

        # Get or create session ID
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id

        # Start step logging in background
        threading.Thread(target=simulate_ai_processing, args=(session_id,), daemon=True).start()

        # Simulate processing delay
        time.sleep(0.5)

        return jsonify({
            "response": f"I received your message: '{message}'. The step logging above shows the processing progress!",
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "chatbot-step-logging-demo",
    })

if __name__ == '__main__':
    port = int(os.getenv('WEB_PORT', 3000))
    print(f"Starting demo chatbot with step logging on port {port}")
    print("Visit http://localhost:3000 to see the step logging UI")
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

