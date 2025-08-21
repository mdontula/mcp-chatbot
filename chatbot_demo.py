#!/usr/bin/env python3
"""
Chatbot Demo Script
Shows examples of how the chatbot processes different types of queries
"""

from chatbot_interface import ChatbotInterface

def demo_chatbot():
    """Demonstrate the chatbot's capabilities"""
    print("🤖 MCP Chatbot Demo")
    print("=" * 60)
    print("This demo shows how the chatbot processes different types of queries")
    print("=" * 60)
    
    chatbot = ChatbotInterface()
    
    # Example queries to test
    demo_queries = [
        # Greetings
        "Hello",
        "Hi there",
        "Hey",
        
        # Help
        "Help",
        "What can you do?",
        "How do you work?",
        
        # Weather queries
        "What's the weather in Tokyo?",
        "How's the weather in London, GB?",
        "Show me the forecast for New York",
        "Weather forecast for Mumbai for 3 days",
        "Temperature in Paris",
        
        # Stock queries
        "What's the stock price of AAPL?",
        "Show me MSFT stock",
        "Stock price for GOOGL",
        "How is TSLA stock doing?",
        "Search for stocks with tech",
        "Find stocks with artificial intelligence",
        
        # News queries
        "Show me top headlines",
        "Get technology news",
        "Business news",
        "Search for news about artificial intelligence",
        "Find news about climate change",
        "News from India",
        "Headlines from United Kingdom",
        
        # Mixed queries
        "What's the weather like in Sydney and show me Apple stock price",
        "Get me the latest technology news and weather in San Francisco",
        
        # Goodbye
        "Goodbye",
        "Bye",
        "See you later"
    ]
    
    print("\n🧪 Testing Chatbot Responses:")
    print("-" * 60)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i:2d}. 👤 User: {query}")
        print("    🤖 Bot: ", end="")
        
        try:
            response = chatbot.process_query(query)
            # Print first 100 characters, then ... if longer
            if len(response) > 100:
                print(response[:100] + "...")
            else:
                print(response)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 60)
    
    print(f"\n✅ Demo completed! Tested {len(demo_queries)} different query types.")
    print("\n💡 Try the interactive chatbot:")
    print("   • Terminal: python chatbot_interface.py")
    print("   • Web: python web_chatbot.py")
    print("   • Startup script: ./start.sh")

if __name__ == "__main__":
    demo_chatbot()
