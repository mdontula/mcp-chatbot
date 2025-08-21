#!/usr/bin/env python3
"""
MCP Chatbot Interface
A conversational chatbot that uses the existing services to answer user queries
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

from services.weather_service import WeatherService
from services.stock_service import StockService
from services.news_service import NewsService
from config import Config

class ChatbotInterface:
    """Main chatbot interface that processes natural language queries"""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.stock_service = StockService()
        self.news_service = NewsService()
        
        # Greeting messages
        self.greetings = [
            "Hello! I'm your MCP chatbot. I can help you with weather, stocks, and news!",
            "Hi there! I'm here to help you get information about weather, stocks, and news.",
            "Welcome! I'm your assistant for real-time information. What would you like to know?"
        ]
        
        # Help messages
        self.help_text = """
🤖 **MCP Chatbot Help**

I can help you with:

🌤️ **Weather Information:**
• "What's the weather in [city]?"
• "How's the weather in [city], [country]?"
• "Show me the forecast for [city]"
• "Weather forecast for [city] for 5 days"

📊 **Stock Information:**
• "What's the stock price of [symbol]?"
• "Show me [AAPL/MSFT/GOOGL] stock"
• "Stock price for [symbol]"
• "Search for stocks with [keyword]"

📰 **News Information:**
• "Show me top headlines"
• "Get [technology/business/sports] news"
• "Search for news about [topic]"
• "Latest news from [country]"

💬 **Conversation:**
• "Hello" / "Hi" / "Hey"
• "Help" / "What can you do?"
• "Thank you" / "Thanks"
• "Goodbye" / "Bye"

Try asking me something like:
• "What's the weather in Tokyo?"
• "Show me Apple stock price"
• "Get technology news"
        """
    
    def process_query(self, user_input: str) -> str:
        """
        Process user input and return appropriate response
        
        Args:
            user_input: User's natural language query
            
        Returns:
            Formatted response string
        """
        # Clean and normalize input
        query = user_input.strip().lower()
        
        # Check for greetings
        if self._is_greeting(query):
            return random.choice(self.greetings)
        
        # Check for help requests
        if self._is_help_request(query):
            return self.help_text
        
        # Check for goodbye
        if self._is_goodbye(query):
            return "Goodbye! Feel free to come back anytime for more information! 👋"
        
        # Check for weather queries
        weather_response = self._handle_weather_query(query)
        if weather_response:
            return weather_response
        
        # Check for stock queries
        stock_response = self._handle_stock_query(query)
        if stock_response:
            return stock_response
        
        # Check for news queries
        news_response = self._handle_news_query(query)
        if news_response:
            return news_response
        
        # If no specific query matched, provide a helpful response
        return self._get_fallback_response(query)
    
    def _is_greeting(self, query: str) -> bool:
        """Check if query is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in query for greeting in greetings)
    
    def _is_help_request(self, query: str) -> bool:
        """Check if query is asking for help"""
        help_terms = ['help', 'what can you do', 'how do you work', 'what are your features']
        return any(term in query for term in help_terms)
    
    def _is_goodbye(self, query: str) -> bool:
        """Check if query is saying goodbye"""
        goodbye_terms = ['goodbye', 'bye', 'see you', 'later', 'exit', 'quit']
        return any(term in query for term in goodbye_terms)
    
    def _handle_weather_query(self, query: str) -> Optional[str]:
        """Handle weather-related queries"""
        
        # Simple, reliable pattern matching
        query_lower = query.lower()
        
        # Check for weather keywords (including common speech recognition errors)
        weather_keywords = [
            'weather', 'whether', 'temperature', 'how is the weather', 'what is the weather',
            'weather in', 'whether in', 'weather for', 'whether for'
        ]
        if not any(keyword in query_lower for keyword in weather_keywords):
            return None
        
        # Extract city and country using simple string operations
        city = None
        country = None
        
        # Look for "in" or "for" to find location
        if ' in ' in query_lower:
            # Extract text after "in"
            in_index = query_lower.find(' in ')
            location_text = query[in_index + 4:].strip()
            
            # Remove common time words that might be attached to city names
            time_words = ['today', 'tomorrow', 'now', 'tonight', 'this week', 'next week']
            for word in time_words:
                if location_text.lower().endswith(word):
                    location_text = location_text[:-len(word)].strip()
            
            # Check if there's a comma (city, country)
            if ',' in location_text:
                parts = location_text.split(',', 1)
                city = parts[0].strip()
                country = parts[1].strip()
            else:
                city = location_text
                
        elif ' for ' in query_lower:
            # Extract text after "for"
            for_index = query_lower.find(' for ')
            location_text = query[for_index + 5:].strip()
            
            # Remove common time words that might be attached to city names
            time_words = ['today', 'tomorrow', 'now', 'tonight', 'this week', 'next week']
            for word in time_words:
                if location_text.lower().endswith(word):
                    location_text = location_text[:-len(word)].strip()
            
            # Check if there's a comma (city, country)
            if ',' in location_text:
                parts = location_text.split(',', 1)
                city = parts[0].strip()
                country = parts[1].strip()
            else:
                city = location_text
        
        # If we found a city, try to get weather
        if city:
            print(f"DEBUG: City extracted: '{city}'")
            print(f"DEBUG: Country extracted: '{country}'")
            print(f"DEBUG: Original query: '{query}'")
            print(f"DEBUG: Query lower: '{query_lower}'")
            
            try:
                result = self.weather_service.get_current_weather(city, country)
                if "error" not in result:
                    return self._format_weather_response(result)
                else:
                    return f"❌ Sorry, I couldn't get weather information for {city}. {result['error']}"
            except Exception as e:
                return f"❌ Sorry, there was an error getting weather for {city}: {str(e)}"
        
        # Check for forecast patterns
        forecast_keywords = ['forecast', '5 day', '3 day', '7 day']
        if any(keyword in query_lower for keyword in forecast_keywords):
            # Extract location and days
            days = 5  # default
            
            # Look for specific day numbers
            day_match = re.search(r'(\d+)\s*day', query_lower)
            if day_match:
                days = int(day_match.group(1))
            
            # Extract location (same logic as above)
            if ' in ' in query_lower:
                in_index = query_lower.find(' in ')
                location_text = query[in_index + 4:].strip()
                
                if ',' in location_text:
                    parts = location_text.split(',', 1)
                    city = parts[0].strip()
                    country = parts[1].strip()
                else:
                    city = location_text
                    
            elif ' for ' in query_lower:
                for_index = query_lower.find(' for ')
                location_text = query[for_index + 5:].strip()
                
                if ',' in location_text:
                    parts = location_text.split(',', 1)
                    city = parts[0].strip()
                    country = parts[1].strip()
                else:
                    city = location_text
            
            if city:
                print(f"DEBUG: Forecast - City: '{city}', Country: '{country}', Days: {days}")
                
                try:
                    result = self.weather_service.get_weather_forecast(city, country, days)
                    if "error" not in result:
                        return self._format_forecast_response(result)
                    else:
                        return f"❌ Sorry, I couldn't get forecast for {city}. {result['error']}"
                except Exception as e:
                    return f"❌ Sorry, there was an error getting forecast for {city}: {str(e)}"
        
        return None
    
    def _handle_stock_query(self, query: str) -> Optional[str]:
        """Handle stock-related queries"""
        
        query_lower = query.lower()
        
        # Check for stock keywords
        stock_keywords = ['stock', 'price', 'stock price', 'how is', 'what is']
        if not any(keyword in query_lower for keyword in stock_keywords):
            return None
        
        # Extract stock symbol or company name
        stock_symbol = None
        
        # Look for "of" to find stock symbol/company
        if ' of ' in query_lower:
            # Extract text after "of"
            of_index = query_lower.find(' of ')
            stock_text = query[of_index + 4:].strip()
            
            # Remove common words and punctuation
            stock_text = stock_text.replace('stock', '').replace('price', '').strip()
            # Remove question marks and other punctuation
            stock_text = stock_text.rstrip('?.,!').strip()
            if stock_text:
                stock_symbol = stock_text
                
        # Look for stock symbol at the beginning (like "AAPL stock" or "Apple stock")
        elif query_lower.startswith(('aapl', 'msft', 'googl', 'amzn', 'tsla', 'meta', 'nvda', 'intc', 'amd')):
            stock_symbol = query_lower.split()[0]
        # Look for company names followed by "stock" (like "Apple stock price")
        elif ' stock' in query_lower:
            stock_index = query_lower.find(' stock')
            stock_text = query[:stock_index].strip()
            # Remove question marks and punctuation
            stock_text = stock_text.rstrip('?.,!').strip()
            if stock_text:
                stock_symbol = stock_text
        
        # If we found a stock symbol, try to get quote
        if stock_symbol:
            print(f"DEBUG: Stock symbol extracted: '{stock_symbol}'")
            print(f"DEBUG: Original query: '{query}'")
            print(f"DEBUG: Query lower: '{query_lower}'")
            
            # First, try to search for the company name to get the symbol
            try:
                search_result = self.stock_service.search_stocks(stock_symbol)
                if "error" not in search_result and search_result.get('results'):
                    # Use the first (best) match
                    best_match = search_result['results'][0]
                    actual_symbol = best_match['symbol']
                    print(f"DEBUG: Found symbol '{actual_symbol}' for '{stock_symbol}'")
                    
                    # Now get the stock quote using the found symbol
                    result = self.stock_service.get_stock_quote(actual_symbol)
                    if "error" not in result:
                        return self._format_stock_response(result)
                    else:
                        return f"❌ Sorry, I couldn't get stock information for {stock_symbol} ({actual_symbol}). {result['error']}"
                else:
                    # Search failed, try direct lookup (might be a direct symbol)
                    print(f"DEBUG: Search failed for '{stock_symbol}', trying direct lookup")
                    result = self.stock_service.get_stock_quote(stock_symbol.upper())
                    if "error" not in result:
                        return self._format_stock_response(result)
                    else:
                        return f"❌ Sorry, I couldn't find stock information for '{stock_symbol}'. Try searching for a different company or use the stock symbol directly."
                        
            except Exception as e:
                return f"❌ Sorry, there was an error searching for stock '{stock_symbol}': {str(e)}"
        
        # Check for stock search patterns
        search_keywords = ['search', 'find', 'stocks with', 'look for']
        if any(keyword in query_lower for keyword in search_keywords):
            # Extract search term
            search_term = None
            
            if ' with ' in query_lower:
                with_index = query_lower.find(' with ')
                search_term = query[with_index + 6:].strip()
            elif ' for ' in query_lower:
                for_index = query_lower.find(' for ')
                search_term = query[for_index + 5:].strip()
            elif ' look for ' in query_lower:
                look_index = query_lower.find(' look for ')
                search_term = query[look_index + 10:].strip()
            
            if search_term:
                print(f"DEBUG: Stock search term extracted: '{search_term}'")
                
                try:
                    result = self.stock_service.search_stocks(search_term)
                    if "error" not in result:
                        return self._format_stock_search_response(result)
                    else:
                        return f"❌ Sorry, I couldn't search for stocks with '{search_term}'. {result['error']}"
                except Exception as e:
                    return f"❌ Sorry, there was an error searching for stocks: {str(e)}"
        
        return None
    
    def _handle_news_query(self, query: str) -> Optional[str]:
        """Handle news-related queries"""
        # Patterns for news queries
        headlines_patterns = [
            r'(?:show\s+me\s+)?(?:top\s+)?headlines?\s*\??',
            r'(?:get\s+)?(?:latest\s+)?news\s*\??',
            r'what\s+is\s+(?:the\s+)?latest\s+news\s*\??',
        ]
        
        category_patterns = [
            r'(?:get\s+)?(technology|business|sports|entertainment|health|science)\s+news\s*\??',
            r'(?:show\s+me\s+)?(technology|business|sports|entertainment|health|science)\s+headlines?\s*\??',
            r'news\s+(?:on\s+)?(technology|business|sports|entertainment|health|science)\s*\??',
            r'news\s+about\s+(technology|business|sports|entertainment|health|science)\s*\??',
        ]
        
        search_patterns = [
            r'search\s+(?:for\s+)?news\s+(?:about\s+)?([a-zA-Z\s]+?)\s*\??',
            r'news\s+(?:about\s+)?([a-zA-Z\s]+?)\s*\??',
            r'find\s+news\s+(?:about\s+)?([a-zA-Z\s]+?)\s*\??',
        ]
        
        country_patterns = [
            r'news\s+from\s+([a-zA-Z\s]+?)\s*\??',
            r'headlines?\s+from\s+([a-zA-Z\s]+?)\s*\??',
        ]
        
        # Check for general headlines
        for pattern in headlines_patterns:
            if re.search(pattern, query):
                try:
                    result = self.news_service.get_top_headlines("us", page_size=5)
                    if "error" not in result:
                        return self._format_news_response(result)
                    else:
                        return f"❌ Sorry, I couldn't get headlines. {result['error']}"
                except Exception as e:
                    return f"❌ Sorry, there was an error getting headlines: {str(e)}"
        
        # Check for category news
        for pattern in category_patterns:
            match = re.search(pattern, query)
            if match:
                category = match.group(1)
                print(f"DEBUG: Category pattern matched: '{pattern}'")
                print(f"DEBUG: Category extracted: '{category}'")
                try:
                    result = self.news_service.get_news_by_category(category, "us", 5)
                    if "error" not in result:
                        return self._format_news_response(result)
                    else:
                        return f"❌ Sorry, I couldn't get {category} news. {result['error']}"
                except Exception as e:
                    return f"❌ Sorry, there was an error getting {category} news: {str(e)}"
        
        # Check for news search
        for pattern in search_patterns:
            match = re.search(pattern, query)
            if match:
                topic = match.group(1).strip()
                try:
                    result = self.news_service.search_news(topic, page_size=5)
                    if "error" not in result:
                        return self._format_news_search_response(result, topic)
                    else:
                        return f"❌ Sorry, I couldn't search for news about '{topic}'. {result['error']}"
                except Exception as e:
                    return f"❌ Sorry, there was an error searching for news: {str(e)}"
        
        # Check for country-specific news
        for pattern in country_patterns:
            match = re.search(pattern, query)
            if match:
                country_name = match.group(1).strip()
                # Try to find country code
                country_code = self._get_country_code(country_name)
                if country_code:
                    try:
                        result = self.news_service.get_top_headlines(country_code, page_size=5)
                        if "error" not in result:
                            return self._format_news_response(result)
                        else:
                            return f"❌ Sorry, I couldn't get news from {country_name}. {result['error']}"
                    except Exception as e:
                        return f"❌ Sorry, there was an error getting news from {country_name}: {str(e)}"
                else:
                    return f"❌ Sorry, I don't recognize '{country_name}' as a country. Try using country codes like 'US', 'GB', 'IN'."
        
        return None
    
    def _get_country_code(self, country_name: str) -> Optional[str]:
        """Get country code from country name"""
        countries = self.news_service.get_available_countries()
        country_name_lower = country_name.lower()
        
        # Direct match
        for code, name in countries.items():
            if country_name_lower == name.lower():
                return code
        
        # Partial match
        for code, name in countries.items():
            if country_name_lower in name.lower() or name.lower() in country_name_lower:
                return code
        
        return None
    
    def _format_weather_response(self, weather: Dict) -> str:
        """Format weather response for chatbot"""
        response = f"🌤️ **Weather in {weather['city']}, {weather['country']}**\n\n"
        response += f"**Current:** {weather['temperature']['current']}°C (feels like {weather['temperature']['feels_like']}°C)\n"
        response += f"**Description:** {weather['description']}\n"
        response += f"**High:** {weather['temperature']['max']}°C, **Low:** {weather['temperature']['min']}°C\n"
        response += f"**Humidity:** {weather['humidity']}%\n"
        response += f"**Wind:** {weather['wind_speed']} m/s\n"
        response += f"**Pressure:** {weather['pressure']} hPa"
        return response
    
    def _format_forecast_response(self, forecast: Dict) -> str:
        """Format forecast response for chatbot"""
        response = f"📅 **Weather Forecast for {forecast['city']}, {forecast['country']}**\n\n"
        
        # Show first 5 forecast periods
        forecasts = forecast['forecasts'][:5]
        for i, day_forecast in enumerate(forecasts, 1):
            response += f"**Day {i}:** {day_forecast['description']}\n"
            response += f"  Temp: {day_forecast['temperature']['current']}°C\n"
            response += f"  Humidity: {day_forecast['humidity']}%\n"
            response += f"  Wind: {day_forecast['wind_speed']} m/s\n\n"
        
        return response
    
    def _format_stock_response(self, stock: Dict) -> str:
        """Format stock response for chatbot"""
        change_emoji = "📈" if stock['change'] >= 0 else "📉"
        
        response = f"{change_emoji} **{stock['symbol']} Stock Information**\n\n"
        response += f"**Current Price:** ${stock['price']:.2f}\n"
        response += f"**Change:** ${stock['change']:.2f} ({stock['change_percent']})\n"
        response += f"**Open:** ${stock['open']:.2f}\n"
        response += f"**High:** ${stock['high']:.2f}\n"
        response += f"**Low:** ${stock['low']:.2f}\n"
        response += f"**Volume:** {stock['volume']:,}\n"
        response += f"**Previous Close:** ${stock['previous_close']:.2f}"
        return response
    
    def _format_stock_search_response(self, search_result: Dict) -> str:
        """Format stock search response for chatbot"""
        response = f"🔍 **Stock Search Results ({search_result['count']} found)**\n\n"
        
        # Show first 5 results
        stocks = search_result['results'][:5]
        for stock in stocks:
            response += f"📊 **{stock['symbol']}** - {stock['name']}\n"
            response += f"   Type: {stock['type']}\n"
            response += f"   Region: {stock['region']}\n"
            response += f"   Currency: {stock['currency']}\n\n"
        
        return response
    
    def _format_news_response(self, news: Dict) -> str:
        """Format news response for chatbot"""
        response = f"📰 **News ({news['count']} articles)**\n\n"
        
        # Show first 5 articles
        articles = news['articles'][:5]
        for i, article in enumerate(articles, 1):
            response += f"{i}. **{article['title']}**\n"
            if article['description']:
                response += f"   {article['description'][:100]}...\n"
            response += f"   Source: {article['source']['name']}\n"
            response += f"   Published: {article['published_at']}\n\n"
        
        return response
    
    def _format_news_search_response(self, news: Dict, topic: str) -> str:
        """Format news search response for chatbot"""
        response = f"🔍 **Search Results for '{topic}' ({news['count']} articles)**\n\n"
        
        # Show first 5 articles
        articles = news['articles'][:5]
        for i, article in enumerate(articles, 1):
            response += f"{i}. **{article['title']}**\n"
            if article['description']:
                response += f"   {article['description'][:100]}...\n"
            response += f"   Source: {article['source']['name']}\n"
            response += f"   Published: {article['published_at']}\n\n"
        
        return response
    
    def _get_fallback_response(self, query: str) -> str:
        """Get a helpful fallback response when query doesn't match"""
        fallback_responses = [
            f"I'm not sure I understood '{query}'. Try asking me about weather, stocks, or news!",
            f"I didn't quite catch that. You can ask me about weather in a city, stock prices, or latest news.",
            f"Could you rephrase that? I can help with weather, stocks, and news information.",
            f"I'm here to help with weather, stocks, and news. Try asking something like 'What's the weather in Tokyo?' or 'Show me Apple stock price'."
        ]
        return random.choice(fallback_responses)

def main():
    """Main function to run the chatbot in interactive mode"""
    chatbot = ChatbotInterface()
    
    print("🤖 MCP Chatbot Interface")
    print("=" * 50)
    print("Type 'help' for assistance or 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 Chatbot: Goodbye! Have a great day! 👋")
                break
            
            if not user_input:
                continue
            
            # Process the query
            response = chatbot.process_query(user_input)
            print(f"\n🤖 Chatbot: {response}")
            
        except KeyboardInterrupt:
            print("\n\n🤖 Chatbot: Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n🤖 Chatbot: Sorry, something went wrong: {str(e)}")

if __name__ == "__main__":
    main()
