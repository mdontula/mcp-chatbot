#!/usr/bin/env python3
"""
Simple test script for MCP Chatbot services
Run this to verify all services are working correctly
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.weather_service import WeatherService
from services.stock_service import StockService
from services.news_service import NewsService
from config import Config

def test_weather_service():
    """Test weather service"""
    print("🌤️ Testing Weather Service...")
    
    weather = WeatherService()
    
    # Test with a simple city
    try:
        result = weather.get_current_weather("London", "GB")
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print(f"   ✅ Success: {result['city']}, {result['country']}")
            print(f"      Temperature: {result['temperature']['current']}°C")
            return True
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_stock_service():
    """Test stock service"""
    print("📊 Testing Stock Service...")
    
    stock = StockService()
    
    # Test with a simple stock symbol
    try:
        result = stock.get_stock_quote("AAPL")
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print(f"   ✅ Success: {result['symbol']}")
            print(f"      Price: ${result['price']:.2f}")
            return True
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_news_service():
    """Test news service"""
    print("📰 Testing News Service...")
    
    news = NewsService()
    
    # Test with simple headlines
    try:
        result = news.get_top_headlines("us", page_size=1)
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print(f"   ✅ Success: Found {result['count']} articles")
            if result['articles']:
                print(f"      First article: {result['articles'][0]['title'][:50]}...")
            return True
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_configuration():
    """Test configuration"""
    print("🔑 Testing Configuration...")
    
    try:
        # Check if API keys are configured
        missing_keys = []
        
        if not Config.OPENWEATHER_API_KEY:
            missing_keys.append("OPENWEATHER_API_KEY")
        if not Config.ALPHA_VANTAGE_API_KEY:
            missing_keys.append("ALPHA_VANTAGE_API_KEY")
        if not Config.NEWS_API_KEY:
            missing_keys.append("NEWS_API_KEY")
        
        if missing_keys:
            print(f"   ⚠️  Missing API keys: {', '.join(missing_keys)}")
            print("      Some services may not work without proper API keys")
            return False
        else:
            print("   ✅ All API keys are configured")
            return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 MCP Chatbot Service Tests")
    print("=" * 50)
    
    # Test configuration first
    config_ok = test_configuration()
    
    if not config_ok:
        print("\n⚠️  Configuration issues detected. Some tests may fail.")
    
    print()
    
    # Test each service
    tests = [
        ("Weather Service", test_weather_service),
        ("Stock Service", test_stock_service),
        ("News Service", test_news_service),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("📋 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MCP chatbot is ready to use.")
        print("\n💡 Next steps:")
        print("   • Run 'python demo.py' to see all features in action")
        print("   • Run 'python web_interface.py' to start the web UI")
        print("   • Run 'python mcp_server.py' to start the MCP server")
    else:
        print("⚠️  Some tests failed. Check the errors above and fix configuration issues.")
        print("\n💡 Common solutions:")
        print("   • Ensure all API keys are set in .env file")
        print("   • Check internet connection")
        print("   • Verify API key validity with respective services")

if __name__ == "__main__":
    main()
