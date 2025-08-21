import requests
from typing import Dict, Optional
from config import Config

class StockService:
    """Service for getting stock information from Alpha Vantage"""
    
    def __init__(self):
        self.api_key = Config.ALPHA_VANTAGE_API_KEY
        self.base_url = Config.ALPHA_VANTAGE_BASE_URL
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get current stock quote for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')
        
        Returns:
            Dictionary containing stock quote information
        """
        if not self.api_key:
            return {"error": "Alpha Vantage API key not configured"}
        
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol.upper(),
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"DEBUG: Alpha Vantage response for {symbol}: {data}")
            
            if 'Global Quote' in data and data['Global Quote']:
                return self._format_stock_quote(data['Global Quote'])
            else:
                return {"error": f"Stock data not found for {symbol}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch stock data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_stock_intraday(self, symbol: str, interval: str = '5min') -> Dict:
        """
        Get intraday stock data
        
        Args:
            symbol: Stock symbol
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
        
        Returns:
            Dictionary containing intraday data
        """
        if not self.api_key:
            return {"error": "Alpha Vantage API key not configured"}
        
        try:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol.upper(),
                'interval': interval,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Time Series (5min)' in data:
                return self._format_intraday_data(data, symbol)
            else:
                return {"error": f"Intraday data not found for {symbol}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch intraday data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def search_stocks(self, keywords: str) -> Dict:
        """
        Search for stocks by keywords
        
        Args:
            keywords: Search keywords
        
        Returns:
            Dictionary containing search results
        """
        if not self.api_key:
            return {"error": "Alpha Vantage API key not configured"}
        
        try:
            params = {
                'function': 'SYMBOL_SEARCH',
                'keywords': keywords,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'bestMatches' in data:
                return self._format_search_results(data['bestMatches'])
            else:
                return {"error": "No search results found"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to search stocks: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _format_stock_quote(self, quote_data: Dict) -> Dict:
        """Format raw stock quote data into a user-friendly format"""
        return {
            "symbol": quote_data.get('01. symbol'),
            "open": float(quote_data.get('02. open', 0)),
            "high": float(quote_data.get('03. high', 0)),
            "low": float(quote_data.get('04. low', 0)),
            "price": float(quote_data.get('05. price', 0)),
            "volume": int(quote_data.get('06. volume', 0)),
            "latest_trading_day": quote_data.get('07. latest trading day'),
            "previous_close": float(quote_data.get('08. previous close', 0)),
            "change": float(quote_data.get('09. change', 0)),
            "change_percent": quote_data.get('10. change percent', '0%')
        }
    
    def _format_intraday_data(self, data: Dict, symbol: str) -> Dict:
        """Format raw intraday data into a user-friendly format"""
        time_series = data.get('Time Series (5min)', {})
        formatted_data = []
        
        for timestamp, values in list(time_series.items())[:20]:  # Last 20 entries
            formatted_data.append({
                "timestamp": timestamp,
                "open": float(values.get('1. open', 0)),
                "high": float(values.get('2. high', 0)),
                "low": float(values.get('3. low', 0)),
                "close": float(values.get('4. close', 0)),
                "volume": int(values.get('5. volume', 0))
            })
        
        return {
            "symbol": symbol,
            "interval": "5min",
            "data": formatted_data
        }
    
    def _format_search_results(self, matches: list) -> Dict:
        """Format search results into a user-friendly format"""
        formatted_matches = []
        
        for match in matches:
            formatted_matches.append({
                "symbol": match.get('1. symbol'),
                "name": match.get('2. name'),
                "type": match.get('3. type'),
                "region": match.get('4. region'),
                "market_open": match.get('5. marketOpen'),
                "market_close": match.get('6. marketClose'),
                "timezone": match.get('7. timezone'),
                "currency": match.get('8. currency')
            })
        
        return {
            "results": formatted_matches,
            "count": len(formatted_matches)
        }
