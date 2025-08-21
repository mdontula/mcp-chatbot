import requests
from typing import Dict, Optional
from config import Config

class WeatherService:
    """Service for getting weather information from OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
    
    def get_current_weather(self, city: str, country_code: str = None) -> Dict:
        """
        Get current weather for a city
        
        Args:
            city: City name
            country_code: Optional country code (e.g., 'US', 'GB')
        
        Returns:
            Dictionary containing weather information
        """
        if not self.api_key:
            return {"error": "OpenWeatherMap API key not configured"}
        
        try:
            # Build location query
            location = city
            if country_code:
                location = f"{city},{country_code}"
            
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'  # Use metric units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('cod') == 200:
                return self._format_weather_data(data)
            else:
                return {"error": f"Weather data not found for {city}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_weather_forecast(self, city: str, country_code: str = None, days: int = 5) -> Dict:
        """
        Get weather forecast for a city
        
        Args:
            city: City name
            country_code: Optional country code
            days: Number of days for forecast (max 5 for free tier)
        
        Returns:
            Dictionary containing forecast information
        """
        if not self.api_key:
            return {"error": "OpenWeatherMap API key not configured"}
        
        try:
            location = city
            if country_code:
                location = f"{city},{country_code}"
            
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 8 forecasts per day, max 40 for free tier
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('cod') == '200':
                return self._format_forecast_data(data, days)
            else:
                return {"error": f"Forecast data not found for {city}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch forecast data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _format_weather_data(self, data: Dict) -> Dict:
        """Format raw weather data into a user-friendly format"""
        weather = data.get('weather', [{}])[0]
        main = data.get('main', {})
        wind = data.get('wind', {})
        
        return {
            "city": data.get('name'),
            "country": data.get('sys', {}).get('country'),
            "description": weather.get('description', '').title(),
            "temperature": {
                "current": round(main.get('temp', 0), 1),
                "feels_like": round(main.get('feels_like', 0), 1),
                "min": round(main.get('temp_min', 0), 1),
                "max": round(main.get('temp_max', 0), 1)
            },
            "humidity": main.get('humidity', 0),
            "pressure": main.get('pressure', 0),
            "wind_speed": round(wind.get('speed', 0), 1),
            "wind_direction": wind.get('deg', 0),
            "visibility": data.get('visibility', 0),
            "sunrise": data.get('sys', {}).get('sunrise'),
            "sunset": data.get('sys', {}).get('sunset'),
            "timestamp": data.get('dt')
        }
    
    def _format_forecast_data(self, data: Dict, days: int) -> Dict:
        """Format raw forecast data into a user-friendly format"""
        forecasts = []
        
        for item in data.get('list', [])[:days * 8]:
            dt = item.get('dt')
            weather = item.get('weather', [{}])[0]
            main = item.get('main', {})
            
            forecast = {
                "datetime": dt,
                "description": weather.get('description', '').title(),
                "temperature": {
                    "current": round(main.get('temp', 0), 1),
                    "feels_like": round(main.get('feels_like', 0), 1),
                    "min": round(main.get('temp_min', 0), 1),
                    "max": round(main.get('temp_max', 0), 1)
                },
                "humidity": main.get('humidity', 0),
                "wind_speed": round(item.get('wind', {}).get('speed', 0), 1)
            }
            forecasts.append(forecast)
        
        return {
            "city": data.get('city', {}).get('name'),
            "country": data.get('city', {}).get('country'),
            "forecasts": forecasts
        }
