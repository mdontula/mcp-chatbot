#!/usr/bin/env python3
"""
Demo script for MCP Chatbot
This script demonstrates the capabilities of the chatbot services
"""

import json
from services.weather_service import WeatherService
from services.stock_service import StockService
from services.news_service import NewsService
from config import Config

def print_separator(title):
    """Print a formatted separator"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demo_weather_service():
    """Demonstrate weather service functionality"""
    print_separator("WEATHER SERVICE DEMO")
    
    weather = WeatherService()
    
    # Test cities
    test_cities = [
        ("New York", "US"),
        ("London", "GB"),
        ("Tokyo", "JP"),
        ("Mumbai", "IN")
    ]
    
    for city, country in test_cities:
        print(f"\n🌤️ Getting weather for {city}, {country}:")
        try:
            result = weather.get_current_weather(city, country)
            if "error" not in result:
                print(f"   Temperature: {result['temperature']['current']}°C")
                print(f"   Description: {result['description']}")
                print(f"   Humidity: {result['humidity']}%")
                print(f"   Wind: {result['wind_speed']} m/s")
            else:
                print(f"   Error: {result['error']}")
        except Exception as e:
            print(f"   Exception: {e}")
    
    # Test forecast
    print(f"\n📅 Getting 3-day forecast for London, GB:")
    try:
        forecast = weather.get_weather_forecast("London", "GB", 3)
        if "error" not in forecast:
            print(f"   Forecast available for {len(forecast['forecasts'])} time periods")
        else:
            print(f"   Error: {forecast['error']}")
    except Exception as e:
        print(f"   Exception: {e}")

def demo_stock_service():
    """Demonstrate stock service functionality"""
    print_separator("STOCK SERVICE DEMO")
    
    stock = StockService()
    
    # Test stock symbols
    test_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
    
    for symbol in test_symbols:
        print(f"\n📊 Getting stock price for {symbol}:")
        try:
            result = stock.get_stock_quote(symbol)
            if "error" not in result:
                print(f"   Price: ${result['price']:.2f}")
                print(f"   Change: ${result['change']:.2f} ({result['change_percent']})")
                print(f"   Volume: {result['volume']:,}")
            else:
                print(f"   Error: {result['error']}")
        except Exception as e:
            print(f"   Exception: {e}")
    
    # Test stock search
    print(f"\n🔍 Searching for stocks with 'tech':")
    try:
        search_result = stock.search_stocks("tech")
        if "error" not in search_result:
            print(f"   Found {search_result['count']} stocks:")
            for stock_info in search_result['results'][:3]:
                print(f"     {stock_info['symbol']}: {stock_info['name']}")
        else:
            print(f"   Error: {search_result['error']}")
    except Exception as e:
        print(f"   Exception: {e}")

def demo_news_service():
    """Demonstrate news service functionality"""
    print_separator("NEWS SERVICE DEMO")
    
    news = NewsService()
    
    # Test top headlines
    print(f"\n📰 Getting top headlines for US:")
    try:
        headlines = news.get_top_headlines("us", page_size=3)
        if "error" not in headlines:
            print(f"   Found {headlines['count']} articles:")
            for i, article in enumerate(headlines['articles'][:3], 1):
                print(f"     {i}. {article['title'][:60]}...")
                print(f"        Source: {article['source']['name']}")
        else:
            print(f"   Error: {headlines['error']}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test news by category
    print(f"\n🔬 Getting technology news for US:")
    try:
        tech_news = news.get_news_by_category("technology", "us", 3)
        if "error" not in tech_news:
            print(f"   Found {tech_news['count']} tech articles:")
            for i, article in enumerate(tech_news['articles'][:3], 1):
                print(f"     {i}. {article['title'][:60]}...")
        else:
            print(f"   Error: {tech_news['error']}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test news search
    print(f"\n🔍 Searching for 'artificial intelligence' news:")
    try:
        search_result = news.search_news("artificial intelligence", page_size=3)
        if "error" not in search_result:
            print(f"   Found {search_result['count']} AI articles:")
            for i, article in enumerate(search_result['articles'][:3], 1):
                print(f"     {i}. {article['title'][:60]}...")
        else:
            print(f"   Error: {search_result['error']}")
    except Exception as e:
        print(f"   Exception: {e}")

def demo_api_info():
    """Show information about available APIs and categories"""
    print_separator("API INFORMATION")
    
    news = NewsService()
    
    print("📰 Available News Categories:")
    categories = news.get_available_categories()
    for category in categories:
        print(f"   • {category}")
    
    print(f"\n🌍 Available Countries (showing first 10):")
    countries = news.get_available_countries()
    for i, (code, name) in enumerate(list(countries.items())[:10]):
        print(f"   • {code}: {name}")

def main():
    """Main demo function"""
    print("🚀 MCP Chatbot Demo")
    print("This script demonstrates the capabilities of the chatbot services")
    
    # Check API keys
    print("\n🔑 Checking API keys...")
    Config.validate_api_keys()
    
    try:
        # Run demos
        demo_weather_service()
        demo_stock_service()
        demo_news_service()
        demo_api_info()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 To use the web interface, run: python web_interface.py")
        print("💡 To use the MCP server, run: python mcp_server.py")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()
