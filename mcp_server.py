import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp import ServerSession, StdioServerParameters
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, ResourceUri, Tool, TextContent, ImageContent, EmbeddedResource
)

from services.weather_service import WeatherService
from services.stock_service import StockService
from services.news_service import NewsService
from config import Config

class MCPServer:
    """Main MCP server that integrates all services"""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.stock_service = StockService()
        self.news_service = NewsService()
        
        # Initialize MCP server
        self.server = Server("mcp-chatbot")
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools with the MCP server"""
        
        # Weather tools
        @self.server.tool()
        async def get_weather(city: str, country_code: str = None) -> str:
            """Get current weather for a city"""
            result = self.weather_service.get_current_weather(city, country_code)
            return self._format_weather_response(result)
        
        @self.server.tool()
        async def get_weather_forecast(city: str, country_code: str = None, days: int = 5) -> str:
            """Get weather forecast for a city (up to 5 days)"""
            result = self.weather_service.get_weather_forecast(city, country_code, days)
            return self._format_forecast_response(result)
        
        # Stock tools
        @self.server.tool()
        async def get_stock_price(symbol: str) -> str:
            """Get current stock price and information for a symbol"""
            result = self.stock_service.get_stock_quote(symbol)
            return self._format_stock_response(result)
        
        @self.server.tool()
        async def search_stocks(keywords: str) -> str:
            """Search for stocks by keywords"""
            result = self.stock_service.search_stocks(keywords)
            return self._format_stock_search_response(result)
        
        @self.server.tool()
        async def get_stock_intraday(symbol: str, interval: str = "5min") -> str:
            """Get intraday stock data for a symbol"""
            result = self.stock_service.get_stock_intraday(symbol, interval)
            return self._format_intraday_response(result)
        
        # News tools
        @self.server.tool()
        async def get_top_headlines(country: str = "us", category: str = None, page_size: int = 10) -> str:
            """Get top news headlines for a country and optional category"""
            result = self.news_service.get_top_headlines(country, category, page_size)
            return self._format_news_response(result)
        
        @self.server.tool()
        async def search_news(query: str, country: str = "us", limit: int = 10) -> str:
            """Search for news articles by query"""
            result = self.news_service.search_news(query, page_size=limit)
            return self._format_news_response(result)
        
        @self.server.tool()
        async def get_news_categories() -> str:
            """Get list of available news categories"""
            categories = self.news_service.get_available_categories()
            return f"Available news categories: {', '.join(categories)}"
        
        @self.server.tool()
        async def get_news_countries() -> str:
            """Get list of available country codes for news"""
            countries = self.news_service.get_available_countries()
            country_list = [f"{code}: {name}" for code, name in list(countries.items())[:20]]
            return f"Available countries (showing first 20):\n" + "\n".join(country_list)
    
    def _format_weather_response(self, result: Dict) -> str:
        """Format weather response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        weather = result
        response = f"🌤️ Weather in {weather['city']}, {weather['country']}\n\n"
        response += f"Current: {weather['temperature']['current']}°C (feels like {weather['temperature']['feels_like']}°C)\n"
        response += f"Description: {weather['description']}\n"
        response += f"High: {weather['temperature']['max']}°C, Low: {weather['temperature']['min']}°C\n"
        response += f"Humidity: {weather['humidity']}%\n"
        response += f"Wind: {weather['wind_speed']} m/s\n"
        response += f"Pressure: {weather['pressure']} hPa"
        
        return response
    
    def _format_forecast_response(self, result: Dict) -> str:
        """Format forecast response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        forecast = result
        response = f"📅 Weather Forecast for {forecast['city']}, {forecast['country']}\n\n"
        
        for i, day_forecast in enumerate(forecast['forecasts'][:5]):
            response += f"Day {i+1}: {day_forecast['description']}\n"
            response += f"  Temp: {day_forecast['temperature']['current']}°C\n"
            response += f"  Humidity: {day_forecast['humidity']}%\n"
            response += f"  Wind: {day_forecast['wind_speed']} m/s\n\n"
        
        return response
    
    def _format_stock_response(self, result: Dict) -> str:
        """Format stock response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        stock = result
        change_emoji = "📈" if stock['change'] >= 0 else "📉"
        
        response = f"{change_emoji} {stock['symbol']} Stock Information\n\n"
        response += f"Current Price: ${stock['price']:.2f}\n"
        response += f"Change: ${stock['change']:.2f} ({stock['change_percent']})\n"
        response += f"Open: ${stock['open']:.2f}\n"
        response += f"High: ${stock['high']:.2f}\n"
        response += f"Low: ${stock['low']:.2f}\n"
        response += f"Volume: {stock['volume']:,}\n"
        response += f"Previous Close: ${stock['previous_close']:.2f}"
        
        return response
    
    def _format_stock_search_response(self, result: Dict) -> str:
        """Format stock search response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        response = f"🔍 Stock Search Results ({result['count']} found)\n\n"
        
        for stock in result['results'][:5]:  # Show first 5 results
            response += f"📊 {stock['symbol']} - {stock['name']}\n"
            response += f"   Type: {stock['type']}\n"
            response += f"   Region: {stock['region']}\n"
            response += f"   Currency: {stock['currency']}\n\n"
        
        return response
    
    def _format_intraday_response(self, result: Dict) -> str:
        """Format intraday response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        response = f"📊 Intraday Data for {result['symbol']}\n\n"
        
        for i, data_point in enumerate(result['data'][:5]):  # Show first 5 data points
            response += f"Time {i+1}: {data_point['timestamp']}\n"
            response += f"  Open: ${data_point['open']:.2f}\n"
            response += f"  High: ${data_point['high']:.2f}\n"
            response += f"  Low: ${data_point['low']:.2f}\n"
            response += f"  Close: ${data_point['close']:.2f}\n"
            response += f"  Volume: {data_point['volume']:,}\n\n"
        
        return response
    
    def _format_news_response(self, result: Dict) -> str:
        """Format news response for display"""
        if "error" in result:
            return f"❌ Error: {result['error']}"
        
        response = f"📰 News ({result['count']} articles)\n\n"
        
        for i, article in enumerate(result['articles'][:5]):  # Show first 5 articles
            response += f"{i+1}. {article['title']}\n"
            if article['description']:
                response += f"   {article['description'][:100]}...\n"
            response += f"   Source: {article['source']['name']}\n"
            response += f"   Published: {article['published_at']}\n\n"
        
        return response
    
    async def run(self):
        """Run the MCP server"""
        # Validate API keys
        api_valid = Config.validate_api_keys()
        if not api_valid:
            print("⚠️  Warning: Some API keys are invalid. The service may not work properly.")
        
        # Start the server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-chatbot",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )

async def main():
    """Main entry point"""
    server = MCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
