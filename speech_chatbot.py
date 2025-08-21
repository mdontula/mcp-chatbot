#!/usr/bin/env python3
"""
Speech-Enabled MCP Web Chatbot
A web-based chatbot with speech-to-text and text-to-speech capabilities
"""

import json
import base64
import tempfile
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from chatbot_interface import ChatbotInterface
from services.speech_service import SpeechService
from config import Config

# Initialize FastAPI app
app = FastAPI(title="MCP Speech Chatbot", version="1.0.0")

# Initialize services
chatbot = ChatbotInterface()
speech_service = SpeechService()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# Request models
class SpeechToTextRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    language: str = "en-US"
    audio_format: str = "webm_opus"  # Audio format hint

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "en-US-Standard-A"
    language: str = "en-US"
    format: str = "mp3"

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def get_speech_chat_interface():
    """Serve the speech-enabled chat interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MCP Speech Chatbot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .chat-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 800px;
                height: 80vh;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }
            
            .chat-header h1 {
                font-size: 24px;
                margin-bottom: 5px;
            }
            
            .chat-header p {
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
            }
            
            .message.user .message-content {
                background: #667eea;
                color: white;
            }
            
            .message.bot .message-content {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
            }
            
            .message-icon {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                margin: 0 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }
            
            .user-icon {
                background: #667eea;
                color: white;
            }
            
            .bot-icon {
                background: #28a745;
                color: white;
            }
            
            .chat-input {
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .input-group {
                flex: 1;
                display: flex;
                gap: 10px;
            }
            
            .text-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            
            .text-input:focus {
                border-color: #667eea;
            }
            
            .btn {
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .btn-primary {
                background: #667eea;
                color: white;
            }
            
            .btn-primary:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
            }
            
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            .btn-secondary:hover {
                background: #5a6268;
            }
            
            .btn-danger {
                background: #dc3545;
                color: white;
            }
            
            .btn-danger:hover {
                background: #c82333;
            }
            
            .btn-warning {
                background: #ffc107;
                color: #333;
            }
            
            .btn-warning:hover {
                background: #e0a800;
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .speech-controls {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .status-indicator {
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
            }
            
            .status-listening {
                background: #ffc107;
                color: #333;
            }
            
            .status-processing {
                background: #17a2b8;
                color: white;
            }
            
            .status-error {
                background: #dc3545;
                color: white;
            }
            
            .audio-player {
                margin-top: 10px;
                width: 100%;
            }
            
            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: white;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
                color: #666;
                font-style: italic;
            }
            
            .typing-indicator.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🎤 MCP Speech Chatbot</h1>
                <p>Your AI assistant with voice capabilities for weather, stocks, and news</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-icon bot-icon">🤖</div>
                    <div class="message-content">
                        Hello! I'm your MCP chatbot with speech capabilities. I can help you with weather, stocks, and news information. 
                        You can type your questions or use the microphone to speak!
                    </div>
                </div>
            </div>
            
            <div class="chat-input">
                <div class="input-group">
                    <input type="text" id="messageInput" class="text-input" 
                           placeholder="Type your message or use voice input..." 
                           onkeypress="handleKeyPress(event)">
                    
                    <button id="sendBtn" class="btn btn-primary" onclick="sendMessage()">
                        📤 Send
                    </button>
                </div>
                
                <button id="micBtn" class="btn btn-secondary" onclick="toggleMicrophone()">
                    🎤 Mic
                </button>
            </div>
            
            <div class="speech-controls" id="speechControls" style="display: none;">
                <div class="status-indicator" id="statusIndicator">Ready</div>
                <button id="stopBtn" class="btn btn-danger" onclick="stopRecording()" style="display: none;">
                    ⏹️ Stop
                </button>
                <button id="stopAudioBtn" class="btn btn-warning" onclick="stopAudio()" style="display: none;">
                    🔇 Stop Audio
                </button>
            </div>
        </div>
        
        <script>
            let ws = null;
            let mediaRecorder = null;
            let audioChunks = [];
            let isRecording = false;
            let isListening = false;
            
            // Initialize WebSocket connection
            function initWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                
                console.log('Attempting to connect to:', wsUrl);
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    console.log('WebSocket connected successfully');
                    document.getElementById('micBtn').disabled = false;
                };
                
                ws.onmessage = function(event) {
                    console.log('Received message:', event.data);
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'bot_message') {
                        addMessage(data.message, 'bot');
                        // Only convert successful responses to speech, not error messages
                        if (!data.message.includes('❌') && !data.message.includes('Sorry, I couldn\'t')) {
                            textToSpeech(data.message);
                        }
                    } else if (data.type === 'speech_result') {
                        addMessage(data.transcript, 'user');
                        // Process the transcribed speech
                        processSpeechQuery(data.transcript);
                    }
                };
                
                ws.onclose = function(event) {
                    console.log('WebSocket disconnected:', event.code, event.reason);
                    document.getElementById('micBtn').disabled = true;
                    // Try to reconnect after 3 seconds
                    setTimeout(initWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                };
            }
            
            // Add message to chat
            function addMessage(message, sender) {
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const icon = sender === 'user' ? '👤' : '🤖';
                const iconClass = sender === 'user' ? 'user-icon' : 'bot-icon';
                
                messageDiv.innerHTML = `
                    <div class="message-icon ${iconClass}">${icon}</div>
                    <div class="message-content">${message}</div>
                `;
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // Send text message
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                // Send via WebSocket
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'user_message',
                        message: message
                    }));
                }
            }
            
            // Handle Enter key
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            // Toggle microphone
            async function toggleMicrophone() {
                if (!isRecording) {
                    await startRecording();
                } else {
                    stopRecording();
                }
            }
            
            // Start recording
            async function startRecording() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ 
                        audio: {
                            sampleRate: 48000,
                            channelCount: 1,
                            echoCancellation: true,
                            noiseSuppression: true
                        } 
                    });
                    
                    // Try different audio formats in order of preference
                    let mimeType = 'audio/webm;codecs=opus';
                    if (!MediaRecorder.isTypeSupported(mimeType)) {
                        mimeType = 'audio/webm';
                        if (!MediaRecorder.isTypeSupported(mimeType)) {
                            mimeType = 'audio/mp4';
                            if (!MediaRecorder.isTypeSupported(mimeType)) {
                                mimeType = 'audio/wav';
                            }
                        }
                    }
                    
                    console.log('Using audio format:', mimeType);
                    
                    mediaRecorder = new MediaRecorder(stream, { mimeType });
                    audioChunks = [];
                    
                    mediaRecorder.ondataavailable = function(event) {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                        }
                    };
                    
                    mediaRecorder.onstop = function() {
                        const audioBlob = new Blob(audioChunks, { type: mimeType });
                        processAudio(audioBlob);
                    };
                    
                    mediaRecorder.start(100); // Collect data every 100ms
                    isRecording = true;
                    
                    // Update UI
                    document.getElementById('micBtn').textContent = '⏹️ Stop';
                    document.getElementById('micBtn').className = 'btn btn-danger';
                    document.getElementById('speechControls').style.display = 'block';
                    document.getElementById('statusIndicator').textContent = 'Listening...';
                    document.getElementById('statusIndicator').className = 'status-indicator status-listening';
                    
                } catch (error) {
                    console.error('Error accessing microphone:', error);
                    alert('Error accessing microphone. Please check permissions.');
                }
            }
            
            // Stop recording
            function stopRecording() {
                if (mediaRecorder && isRecording) {
                    mediaRecorder.stop();
                    isRecording = false;
                    
                    // Update UI
                    document.getElementById('micBtn').textContent = '🎤 Mic';
                    document.getElementById('micBtn').className = 'btn btn-secondary';
                    document.getElementById('statusIndicator').textContent = 'Processing...';
                    document.getElementById('statusIndicator').className = 'status-indicator status-processing';
                }
            }
            
            // Process recorded audio
            async function processAudio(audioBlob) {
                try {
                    console.log('Processing audio blob:', audioBlob.size, 'bytes, type:', audioBlob.type);
                    
                    // Convert audio to base64
                    const reader = new FileReader();
                    reader.onload = function() {
                        const base64Audio = reader.result.split(',')[1];
                        console.log('Audio converted to base64, length:', base64Audio.length);
                        
                        // Send to server for speech recognition
                        fetch('/speech-to-text', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                audio_data: base64Audio,
                                language: 'en-US',
                                audio_format: audioBlob.type
                            })
                        })
                        .then(response => {
                            console.log('Speech API response status:', response.status);
                            return response.json();
                        })
                        .then(data => {
                            console.log('Speech API response:', data);
                            if (data.success) {
                                document.getElementById('statusIndicator').textContent = 'Ready';
                                document.getElementById('statusIndicator').className = 'status-indicator';
                                document.getElementById('speechControls').style.display = 'none';
                                
                                // Send transcript to WebSocket
                                if (ws && ws.readyState === WebSocket.OPEN) {
                                    ws.send(JSON.stringify({
                                        type: 'speech_result',
                                        transcript: data.transcript
                                    }));
                                }
                            } else {
                                throw new Error(data.error);
                            }
                        })
                        .catch(error => {
                            console.error('Speech recognition error:', error);
                            document.getElementById('statusIndicator').textContent = 'Error: ' + error.message;
                            document.getElementById('statusIndicator').className = 'status-indicator status-error';
                        });
                    };
                    
                    reader.onerror = function(error) {
                        console.error('Error reading audio file:', error);
                        document.getElementById('statusIndicator').textContent = 'Error reading audio';
                        document.getElementById('statusIndicator').className = 'status-indicator status-error';
                    };
                    
                    reader.readAsDataURL(audioBlob);
                    
                } catch (error) {
                    console.error('Error processing audio:', error);
                    document.getElementById('statusIndicator').textContent = 'Error processing audio';
                    document.getElementById('statusIndicator').className = 'status-indicator status-error';
                }
            }
            
            // Process speech query
            function processSpeechQuery(transcript) {
                console.log('Processing speech query:', transcript);
                
                // Send the transcribed text to the chatbot
                if (ws && ws.readyState === WebSocket.OPEN) {
                    console.log('Sending transcript to WebSocket:', transcript);
                    ws.send(JSON.stringify({
                        type: 'user_message',
                        message: transcript
                    }));
                } else {
                    console.error('WebSocket not connected, cannot send transcript');
                }
            }
            
            // Global audio element for control
            let currentAudio = null;
            
            // Convert text to speech
            async function textToSpeech(text) {
                try {
                    // Stop any currently playing audio
                    if (currentAudio) {
                        currentAudio.pause();
                        currentAudio = null;
                    }
                    
                    // Show stop audio button
                    document.getElementById('stopAudioBtn').style.display = 'inline-block';
                    
                    const response = await fetch('/text-to-speech', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: text,
                            voice: 'en-US-Standard-A',
                            language: 'en-US',
                            format: 'mp3'
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Create audio element and play
                        currentAudio = new Audio('data:audio/mp3;base64,' + data.audio_data);
                        
                        currentAudio.onended = function() {
                            // Hide stop button when audio finishes
                            document.getElementById('stopAudioBtn').style.display = 'none';
                            currentAudio = null;
                        };
                        
                        currentAudio.play();
                    }
                    
                } catch (error) {
                    console.error('Text-to-speech error:', error);
                    // Hide stop button on error
                    document.getElementById('stopAudioBtn').style.display = 'none';
                }
            }
            
            // Stop audio playback
            function stopAudio() {
                if (currentAudio) {
                    currentAudio.pause();
                    currentAudio = null;
                    document.getElementById('stopAudioBtn').style.display = 'none';
                }
            }
            
            // Initialize when page loads
            window.onload = function() {
                initWebSocket();
            };
        </script>
    </body>
    </html>
    """

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    
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
                response_data = {
                    'type': 'bot_message',
                    'message': bot_response
                }
                print(f"Sending response: {response_data}")
                await websocket.send_text(json.dumps(response_data))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Speech-to-text endpoint
@app.post("/speech-to-text")
async def speech_to_text(request: SpeechToTextRequest):
    """Convert speech audio to text"""
    try:
        # Decode base64 audio
        audio_data = base64.b64decode(request.audio_data)
        
        # Convert speech to text with format hint
        result = speech_service.speech_to_text(audio_data, request.language, request.audio_format)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Text-to-speech endpoint
@app.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """Convert text to speech"""
    try:
        # Convert text to speech
        result = speech_service.text_to_speech(
            request.text, 
            request.voice, 
            request.language, 
            request.format
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get available voices
@app.get("/voices")
async def get_voices(language: str = "en-US"):
    """Get available voices for a language"""
    return speech_service.get_available_voices(language)

# Get supported languages
@app.get("/languages")
async def get_languages():
    """Get list of supported languages"""
    return speech_service.get_supported_languages()

if __name__ == "__main__":
    # Validate configuration
    print("🔍 Validating configuration...")
    
    api_valid = Config.validate_api_keys()
    print(f"API Keys: {'✅ Valid' if api_valid else '❌ Invalid'}")
    
    google_valid = Config.validate_google_cloud()
    print(f"Google Cloud: {'✅ Valid' if google_valid else '❌ Invalid'}")
    
    if not google_valid:
        print("⚠️  Warning: Speech features will not work without Google Cloud credentials")
        print("💡 To enable speech features:")
        print("   1. Create a Google Cloud project")
        print("   2. Enable Speech-to-Text and Text-to-Speech APIs")
        print("   3. Create a service account and download credentials")
        print("   4. Set GOOGLE_APPLICATION_CREDENTIALS in your .env file")
    
    print("\n🚀 Starting MCP Speech Chatbot...")
    print(f"🌐 Web interface will be available at: http://localhost:8002")
    print(f"💬 Speech chat interface will be available at: http://localhost:8002")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
