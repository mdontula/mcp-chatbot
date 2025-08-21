from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from services.weather_service import WeatherService
from services.stock_service import StockService
from services.news_service import NewsService
from config import Config

app = FastAPI(title="MCP Chatbot Web Interface", version="1.0.0")

# Initialize services
weather_service = WeatherService()
stock_service = StockService()
news_service = NewsService()

class WeatherRequest(BaseModel):
    city: str
    country_code: Optional[str] = None

class StockRequest(BaseModel):
    symbol: str

class NewsRequest(BaseModel):
    query: Optional[str] = None
    country: str = "us"
    category: Optional[str] = None
    limit: int = 5

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main page with interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Chatbot</title>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .form-group { margin: 10px 0; }
            label { display: inline-block; width: 120px; }
            input, select { padding: 5px; width: 200px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>🌤️ MCP Chatbot Web Interface</h1>
        
        <div class="section">
            <h2>🌦️ Weather Information</h2>
            <div class="form-group">
                <label>City:</label>
                <input type="text" id="weatherCity" placeholder="e.g., New York">
            </div>
            <div class="form-group">
                <label>Country Code:</label>
                <input type="text" id="weatherCountry" placeholder="e.g., US (optional)">
            </div>
            <button onclick="getWeather()">Get Weather</button>
            <button onclick="getForecast()">Get Forecast</button>
            <div id="weatherResult" class="result"></div>
        </div>
        
        <div class="section">
            <h2>📊 Stock Information</h2>
            <div class="form-group">
                <label>Stock Symbol:</label>
                <input type="text" id="stockSymbol" placeholder="e.g., AAPL">
            </div>
            <button onclick="getStockPrice()">Get Stock Price</button>
            <button onclick="getStockIntraday()">Get Intraday Data</button>
            <div id="stockResult" class="result"></div>
        </div>
        
        <div class="section">
            <h2>📰 News Information</h2>
            <div class="form-group">
                <label>Query:</label>
                <input type="text" id="newsQuery" placeholder="e.g., technology (optional)">
            </div>
            <div class="form-group">
                <label>Country:</label>
                <select id="newsCountry">
                    <option value="us">United States</option>
                    <option value="gb">United Kingdom</option>
                    <option value="in">India</option>
                    <option value="ca">Canada</option>
                    <option value="au">Australia</option>
                </select>
            </div>
            <div class="form-group">
                <label>Category:</label>
                <select id="newsCategory">
                    <option value="">All Categories</option>
                    <option value="business">Business</option>
                    <option value="technology">Technology</option>
                    <option value="sports">Sports</option>
                    <option value="entertainment">Entertainment</option>
                    <option value="health">Health</option>
                    <option value="science">Science</option>
                </select>
            </div>
            <button onclick="getTopHeadlines()">Get Top Headlines</button>
            <button onclick="searchNews()">Search News</button>
            <div id="newsResult" class="result"></div>
        </div>
        
        <script>
            // Version: 1.1 - Force cache refresh
            console.log('MCP Chatbot Web Interface loaded - Version 1.1');
            
            async function apiCall(endpoint, data) {
                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    const result = await response.json();
                    return result;
                } catch (error) {
                    return { error: 'Network error: ' + error.message };
                }
            }
            
            async function getWeather() {
                const city = document.getElementById('weatherCity').value;
                const country = document.getElementById('weatherCountry').value;
                if (!city) {
                    showResult('weatherResult', 'Please enter a city name', true);
                    return;
                }
                
                const data = { city: city };
                if (country) data.country_code = country;
                
                const result = await apiCall('/weather/current', data);
                if (result.error) {
                    showResult('weatherResult', result.error, true);
                } else if (result.result) {
                    // Format the weather data nicely
                    const weather = result.result;
                    let formattedResult = `🌤️ Weather in ${weather.city}, ${weather.country}\n\n`;
                    formattedResult += `Current: ${weather.temperature.current}°C (feels like ${weather.temperature.feels_like}°C)\n`;
                    formattedResult += `Description: ${weather.description}\n`;
                    formattedResult += `High: ${weather.temperature.max}°C, Low: ${weather.temperature.min}°C\n`;
                    formattedResult += `Humidity: ${weather.humidity}%\n`;
                    formattedResult += `Wind: ${weather.wind_speed} m/s\n`;
                    formattedResult += `Pressure: ${weather.pressure} hPa`;
                    showResult('weatherResult', formattedResult, false);
                } else {
                    showResult('weatherResult', 'Unexpected response format', true);
                }
            }
            
            async function getForecast() {
                const city = document.getElementById('weatherCity').value;
                const country = document.getElementById('weatherCountry').value;
                if (!city) {
                    showResult('weatherResult', 'Please enter a city name', true);
                    return;
                }
                
                const data = { city: city };
                if (country) data.country_code = country;
                
                const result = await apiCall('/weather/forecast', data);
                if (result.error) {
                    showResult('weatherResult', result.error, true);
                } else if (result.result) {
                    // Format the forecast data nicely
                    const forecast = result.result;
                    let formattedResult = `📅 Weather Forecast for ${forecast.city}, ${forecast.country}\n\n`;
                    
                    // Show first 5 forecast periods
                    const forecasts = forecast.forecasts.slice(0, 5);
                    forecasts.forEach((dayForecast, index) => {
                        formattedResult += `Day ${index + 1}: ${dayForecast.description}\n`;
                        formattedResult += `  Temp: ${dayForecast.temperature.current}°C\n`;
                        formattedResult += `  Humidity: ${dayForecast.humidity}%\n`;
                        formattedResult += `  Wind: ${dayForecast.wind_speed} m/s\n\n`;
                    });
                    
                    showResult('weatherResult', formattedResult, false);
                } else {
                    showResult('weatherResult', 'Unexpected response format', true);
                }
            }
            
            async function getStockPrice() {
                const symbol = document.getElementById('stockSymbol').value;
                if (!symbol) {
                    showResult('stockResult', 'Please enter a stock symbol', true);
                    return;
                }
                
                const result = await apiCall('/stock/quote', { symbol: symbol });
                if (result.error) {
                    showResult('stockResult', result.error, true);
                } else if (result.result) {
                    // Format the stock data nicely
                    const stock = result.result;
                    const changeEmoji = stock.change >= 0 ? '📈' : '📉';
                    let formattedResult = `${changeEmoji} ${stock.symbol} Stock Information\n\n`;
                    formattedResult += `Current Price: $${stock.price.toFixed(2)}\n`;
                    formattedResult += `Change: $${stock.change.toFixed(2)} (${stock.change_percent})\n`;
                    formattedResult += `Open: $${stock.open.toFixed(2)}\n`;
                    formattedResult += `High: $${stock.high.toFixed(2)}\n`;
                    formattedResult += `Low: $${stock.low.toFixed(2)}\n`;
                    formattedResult += `Volume: ${stock.volume.toLocaleString()}\n`;
                    formattedResult += `Previous Close: $${stock.previous_close.toFixed(2)}`;
                    showResult('stockResult', formattedResult, false);
                } else {
                    showResult('stockResult', 'Unexpected response format', true);
                }
            }
            
            async function getStockIntraday() {
                const symbol = document.getElementById('stockSymbol').value;
                if (!symbol) {
                    showResult('stockResult', 'Please enter a stock symbol', true);
                    return;
                }
                
                const result = await apiCall('/stock/intraday', { symbol: symbol });
                if (result.error) {
                    showResult('stockResult', result.error, true);
                } else if (result.result) {
                    // Format the intraday data nicely
                    const intraday = result.result;
                    let formattedResult = `📊 Intraday Data for ${intraday.symbol}\n\n`;
                    
                    // Show first 5 data points
                    const dataPoints = intraday.data.slice(0, 5);
                    dataPoints.forEach((dataPoint, index) => {
                        formattedResult += `Time ${index + 1}: ${dataPoint.timestamp}\n`;
                        formattedResult += `  Open: $${dataPoint.open.toFixed(2)}\n`;
                        formattedResult += `  High: $${dataPoint.high.toFixed(2)}\n`;
                        formattedResult += `  Low: $${dataPoint.low.toFixed(2)}\n`;
                        formattedResult += `  Close: $${dataPoint.close.toFixed(2)}\n`;
                        formattedResult += `  Volume: ${dataPoint.volume.toLocaleString()}\n\n`;
                    });
                    
                    showResult('stockResult', formattedResult, false);
                } else {
                    showResult('stockResult', 'Unexpected response format', true);
                }
            }
            
            async function getTopHeadlines() {
                const country = document.getElementById('newsCountry').value;
                const category = document.getElementById('newsCategory').value;
                
                const data = { country: country, limit: 5 };
                if (category) data.category = category;
                
                const result = await apiCall('/news/headlines', data);
                if (result.error) {
                    showResult('newsResult', result.error, true);
                } else if (result.result) {
                    // Format the news data nicely
                    const news = result.result;
                    let formattedResult = `📰 News (${news.count} articles)\n\n`;
                    
                    // Show first 5 articles
                    const articles = news.articles.slice(0, 5);
                    articles.forEach((article, index) => {
                        formattedResult += `${index + 1}. ${article.title}\n`;
                        if (article.description) {
                            formattedResult += `   ${article.description.substring(0, 100)}...\n`;
                        }
                        formattedResult += `   Source: ${article.source.name}\n`;
                        formattedResult += `   Published: ${article.published_at}\n\n`;
                    });
                    
                    showResult('newsResult', formattedResult, false);
                } else {
                    showResult('newsResult', 'Unexpected response format', true);
                }
            }
            
            async function searchNews() {
                const query = document.getElementById('newsQuery').value;
                const country = document.getElementById('newsCountry').value;
                
                if (!query) {
                    showResult('newsResult', 'Please enter a search query', true);
                    return;
                }
                
                const result = await apiCall('/news/search', { 
                    query: query, 
                    country: country, 
                    limit: 5 
                });
                if (result.error) {
                    showResult('newsResult', result.error, true);
                } else if (result.result) {
                    // Format the search results nicely
                    const news = result.result;
                    let formattedResult = `🔍 Search Results for "${query}" (${news.count} articles)\n\n`;
                    
                    // Show first 5 articles
                    const articles = news.articles.slice(0, 5);
                    articles.forEach((article, index) => {
                        formattedResult += `${index + 1}. ${article.title}\n`;
                        if (article.description) {
                            formattedResult += `   ${article.description.substring(0, 100)}...\n`;
                        }
                        formattedResult += `   Source: ${article.source.name}\n`;
                        formattedResult += `   Published: ${article.published_at}\n\n`;
                    });
                    
                    showResult('newsResult', formattedResult, false);
                } else {
                    showResult('newsResult', 'Unexpected response format', true);
                }
            }
            
            function showResult(elementId, text, isError = false) {
                const element = document.getElementById(elementId);
                console.log('showResult called with:', { elementId, text, isError, type: typeof text });
                
                // Handle both string and object responses
                if (typeof text === 'object') {
                    element.textContent = JSON.stringify(text, null, 2);
                } else {
                    element.textContent = text;
                }
                element.className = 'result' + (isError ? ' error' : '');
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/weather/current")
async def get_current_weather(request: WeatherRequest):
    """Get current weather for a city"""
    try:
        result = weather_service.get_current_weather(request.city, request.country_code)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/weather/forecast")
async def get_weather_forecast(request: WeatherRequest):
    """Get weather forecast for a city"""
    try:
        result = weather_service.get_weather_forecast(request.city, request.country_code)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stock/quote")
async def get_stock_quote(request: StockRequest):
    """Get stock quote for a symbol"""
    try:
        result = stock_service.get_stock_quote(request.symbol)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stock/intraday")
async def get_stock_intraday(request: StockRequest):
    """Get intraday stock data for a symbol"""
    try:
        result = stock_service.get_stock_intraday(request.symbol)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/news/headlines")
async def get_top_headlines(request: NewsRequest):
    """Get top news headlines"""
    try:
        result = news_service.get_top_headlines(
            request.country, 
            request.category, 
            request.limit
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/news/search")
async def search_news(request: NewsRequest):
    """Search for news articles"""
    try:
        result = news_service.search_news(
            request.query, 
            page_size=request.limit
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "services": ["weather", "stock", "news"]}

if __name__ == "__main__":
    # Validate API keys before starting
    api_valid = Config.validate_api_keys()
    if not api_valid:
        print("⚠️  Warning: Some API keys are invalid. The service may not work properly.")
    
    print("Starting MCP Chatbot Web Interface...")
    print(f"Server will be available at: http://{Config.HOST}:{Config.PORT}")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
