#!/bin/bash

# MCP Chatbot Startup Script
# This script helps you start the chatbot in different modes

set -e

echo "🚀 MCP Chatbot Startup Script"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please run this script from the mcp-chatbot directory."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from template."
        echo "📝 Please edit .env file with your API keys before continuing."
        echo "   Required keys: OPENWEATHER_API_KEY, ALPHA_VANTAGE_API_KEY, NEWS_API_KEY"
        read -p "Press Enter after editing .env file..."
    else
        echo "❌ env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
if ! python3 -c "import mcp, fastapi, requests" &> /dev/null; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Function to start web interface
start_web() {
    echo "🌐 Starting Web Interface..."
    echo "   URL: http://localhost:8000"
    echo "   Press Ctrl+C to stop"
    python3 web_interface.py
}

# Function to start MCP server
start_mcp() {
    echo "🔌 Starting MCP Server..."
    echo "   This will start the MCP server for AI assistant integration"
    echo "   Press Ctrl+C to stop"
    python3 mcp_server.py
}

# Function to run demo
run_demo() {
    echo "🎯 Running Demo..."
    python3 demo.py
}

    # Function to run tests
    run_tests() {
        echo "🧪 Running Tests..."
        python3 test_services.py
    }
    
    # Function to start terminal chatbot
    start_terminal_chatbot() {
        echo "🤖 Starting Terminal Chatbot..."
        echo "   Type 'help' for assistance or 'quit' to exit"
        python3 chatbot_interface.py
    }
    
    # Function to start web chatbot
    start_web_chatbot() {
        echo "💬 Starting Web Chatbot..."
        echo "   Chat interface will be available at: http://localhost:8001"
        echo "   Press Ctrl+C to stop"
        python3 web_chatbot.py
    }
    
    # Function to start speech chatbot
    start_speech_chatbot() {
        echo "🎤 Starting Speech Chatbot..."
        echo "   Speech-enabled chat interface will be available at: http://localhost:8002"
        echo "   Press Ctrl+C to stop"
        python3 speech_chatbot.py
    }

# Main menu
while true; do
    echo ""
            echo "Choose an option:"
        echo "1) 🌐 Start Web Interface"
        echo "2) 🔌 Start MCP Server"
        echo "3) 🎯 Run Demo"
        echo "4) 🧪 Run Tests"
        echo "5) 🤖 Start Terminal Chatbot"
        echo "6) 💬 Start Web Chatbot"
        echo "7) 🎤 Start Speech Chatbot"
        echo "8) 📋 Show Status"
        echo "9) ❌ Exit"
    echo ""
            read -p "Enter your choice (1-9): " choice
    
            case $choice in
            1)
                start_web
                break
                ;;
            2)
                start_mcp
                break
                ;;
            3)
                run_demo
                break
                ;;
            4)
                run_tests
                break
                ;;
            5)
                start_terminal_chatbot
                break
                ;;
            6)
                start_web_chatbot
                break
                ;;
            7)
                start_speech_chatbot
                break
                ;;
            8)
                echo ""
                echo "📋 Current Status:"
                echo "   Python version: $(python3 --version)"
                echo "   Working directory: $(pwd)"
                echo "   .env file: $(if [ -f ".env" ]; then echo "✅ Found"; else echo "❌ Missing"; fi)"
                echo "   Requirements: $(if [ -f "requirements.txt" ]; then echo "✅ Found"; else echo "❌ Missing"; fi)"
                echo ""
                ;;
            9)
                echo "👋 Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice. Please enter 1-9."
                ;;
        esac
done
