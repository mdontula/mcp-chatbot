import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the MCP chatbot"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # API Base URLs
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not cls.OPENWEATHER_API_KEY:
            missing_keys.append("OPENWEATHER_API_KEY")
        if not cls.ALPHA_VANTAGE_API_KEY:
            missing_keys.append("ALPHA_VANTAGE_API_KEY")
        if not cls.NEWS_API_KEY:
            missing_keys.append("NEWS_API_KEY")
            
        if missing_keys:
            print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
            print("Some features may not work without proper API keys.")
            return False
        return True
    
    @classmethod
    def validate_google_cloud(cls):
        """Validate Google Cloud configuration"""
        if not cls.GOOGLE_APPLICATION_CREDENTIALS:
            print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set")
            print("Speech features will not work without Google Cloud credentials.")
            return False
        if not os.path.exists(cls.GOOGLE_APPLICATION_CREDENTIALS):
            print(f"Warning: Google Cloud credentials file not found: {cls.GOOGLE_APPLICATION_CREDENTIALS}")
            print("Speech features will not work without valid credentials.")
            return False
        print("Google Cloud credentials configured successfully.")
        return True
