#!/usr/bin/env python3
"""
Web-based Chatbot Interface
A real-time chat interface using FastAPI and WebSocket
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
from typing import List

from chatbot_interface import ChatbotInterface

app = FastAPI(title="MCP Web Chatbot", version="1.0.0")

# Initialize chatbot
chatbot = ChatbotInterface()

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_chatbot_interface():
    """Main chatbot interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Web Chatbot</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .chat-container {
                width: 90%;
                max-width: 800px;
                height: 80vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 20px 20px 0 0;
            }
            
            .chat-header h1 {
                margin: 0;
                font-size: 24px;
                font-weight: 300;
            }
            
            .chat-header p {
                margin: 5px 0 0 0;
                opacity: 0.9;
                font-size: 14px;
            }
            
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
            }
            
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            
            .message.user {
                justify-content: flex-end;
            }
            
            .message.bot {
                justify-content: flex-start;
            }
            
            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
                line-height: 1.4;
            }
            
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 6px;
            }
            
            .message.bot .message-content {
                background: white;
                color: #333;
                border: 1px solid #e1e5e9;
                border-bottom-left-radius: 6px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                margin: 0 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                font-weight: bold;
            }
            
            .message.user .message-avatar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .message.bot .message-avatar {
                background: #28a745;
                color: white;
            }
            
            .chat-input-container {
                padding: 20px;
                background: white;
                border-top: 1px solid #e1e5e9;
            }
            
            .chat-input-form {
                display: flex;
                gap: 10px;
            }
            
            .chat-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e1e5e9;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            
            .chat-input:focus {
                border-color: #667eea;
            }
            
            .send-button {
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            
            .send-button:hover {
                transform: translateY(-2px);
            }
            
            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: white;
                border: 1px solid #e1e5e9;
                border-radius: 18px;
                border-bottom-left-radius: 6px;
                margin-bottom: 15px;
                color: #666;
                font-style: italic;
            }
            
            .typing-indicator.show {
                display: block;
            }
            
            .help-text {
                background: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                font-size: 14px;
                line-height: 1.5;
            }
            
            .help-text h3 {
                margin: 0 0 10px 0;
                color: #1976d2;
            }
            
            .help-text ul {
                margin: 0;
                padding-left: 20px;
            }
            
            .help-text li {
                margin-bottom: 5px;
            }
            
            @media (max-width: 768px) {
                .chat-container {
                    width: 95%;
                    height: 90vh;
                }
                
                .message-content {
                    max-width: 85%;
                }
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🤖 MCP Chatbot</h1>
                <p>Your AI assistant for weather, stocks, and news</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="help-text">
                    <h3>💡 How to use this chatbot:</h3>
                    <ul>
                        <li><strong>Weather:</strong> "What's the weather in Tokyo?" or "Show me forecast for London"</li>
                        <li><strong>Stocks:</strong> "Show me AAPL stock price" or "Search for tech stocks"</li>
                        <li><strong>News:</strong> "Get technology news" or "Search for AI news"</li>
                        <li><strong>General:</strong> "Hello", "Help", or "What can you do?"</li>
                    </ul>
                </div>
                
                <div class="message bot">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        Hello! I'm your MCP chatbot. I can help you with weather, stocks, and news information. What would you like to know?
                    </div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                🤖 Bot is typing...
            </div>
            
            <div class="chat-input-container">
                <form class="chat-input-form" id="chatForm">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Ask me about weather, stocks, or news..." autocomplete="off">
                    <button type="submit" class="send-button" id="sendButton">Send</button>
                </form>
            </div>
        </div>
        
        <script>
            const chatMessages = document.getElementById('chatMessages');
            const chatForm = document.getElementById('chatForm');
            const chatInput = document.getElementById('chatInput');
            const sendButton = document.getElementById('sendButton');
            const typingIndicator = document.getElementById('typingIndicator');
            
            let ws = null;
            
            // Initialize WebSocket connection
            function initWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                
                console.log('Attempting to connect to:', wsUrl);
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    console.log('WebSocket connected successfully');
                    hideTypingIndicator();
                };
                
                ws.onmessage = function(event) {
                    console.log('Received message:', event.data);
                    const data = JSON.parse(event.data);
                    if (data.type === 'bot_message') {
                        addMessage(data.message, 'bot');
                        hideTypingIndicator();
                    }
                };
                
                ws.onclose = function(event) {
                    console.log('WebSocket disconnected:', event.code, event.reason);
                    // Try to reconnect after 3 seconds
                    setTimeout(initWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            }
            
            // Add message to chat
            function addMessage(message, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const avatar = document.createElement('div');
                avatar.className = 'message-avatar';
                avatar.textContent = sender === 'user' ? '👤' : '🤖';
                
                const content = document.createElement('div');
                content.className = 'message-content';
                content.innerHTML = message.replace(/\\n/g, '<br>');
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(content);
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // Show typing indicator
            function showTypingIndicator() {
                typingIndicator.classList.add('show');
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // Hide typing indicator
            function hideTypingIndicator() {
                typingIndicator.classList.remove('show');
            }
            
            // Handle form submission
            chatForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const message = chatInput.value.trim();
                if (!message) return;
                
                // Add user message
                addMessage(message, 'user');
                
                // Clear input
                chatInput.value = '';
                
                // Show typing indicator
                showTypingIndicator();
                
                // Send message via WebSocket
                if (ws && ws.readyState === WebSocket.OPEN) {
                    console.log('Sending message via WebSocket:', message);
                    ws.send(JSON.stringify({
                        type: 'user_message',
                        message: message
                    }));
                } else {
                    // Fallback: simulate response
                    console.log('WebSocket not available, using fallback');
                    setTimeout(() => {
                        hideTypingIndicator();
                        addMessage('Sorry, WebSocket connection is not available. Please refresh the page.', 'bot');
                    }, 1000);
                }
            });
            
            // Initialize WebSocket when page loads
            window.addEventListener('load', initWebSocket);
            
            // Auto-focus input
            chatInput.focus();
        </script>
    </body>
    </html>
    """
    return html_content

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    print(f"WebSocket connected. Total connections: {len(manager.active_connections)}")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data['type'] == 'user_message':
                user_message = message_data['message']
                print(f"Received message: {user_message}")
                
                # Process message with chatbot
                bot_response = chatbot.process_query(user_message)
                print(f"Bot response: {bot_response[:100]}...")
                
                # Send bot response back
                await websocket.send_text(json.dumps({
                    'type': 'bot_message',
                    'message': bot_response
                }))
                
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "web_chatbot"}

if __name__ == "__main__":
    print("🤖 Starting MCP Web Chatbot...")
    print("🌐 Web interface will be available at: http://localhost:8001")
    print("💬 Chat interface will be available at: http://localhost:8001")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
