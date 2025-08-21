import requests
from typing import Dict, Optional, List
from config import Config

class NewsService:
    """Service for getting news information from NewsAPI.org"""
    
    def __init__(self):
        self.api_key = Config.NEWS_API_KEY
        self.base_url = Config.NEWS_API_BASE_URL
    
    def get_top_headlines(self, country: str = 'us', category: str = None, page_size: int = 10) -> Dict:
        """
        Get top headlines for a country
        
        Args:
            country: Country code (e.g., 'us', 'gb', 'in')
            category: News category (business, entertainment, general, health, science, sports, technology)
            page_size: Number of articles to return (max 100 for free tier)
        
        Returns:
            Dictionary containing top headlines
        """
        if not self.api_key:
            return {"error": "NewsAPI key not configured"}
        
        try:
            params = {
                'country': country.lower(),
                'pageSize': min(page_size, 100),
                'apiKey': self.api_key
            }
            
            if category:
                params['category'] = category.lower()
            
            url = f"{self.base_url}/top-headlines"
            print(f"DEBUG: NewsAPI call - URL: {url}")
            print(f"DEBUG: NewsAPI call - Params: {params}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"DEBUG: NewsAPI response status: {data.get('status')}")
            print(f"DEBUG: NewsAPI response articles count: {len(data.get('articles', []))}")
            
            if data.get('status') == 'ok':
                return self._format_headlines(data)
            else:
                return {"error": f"Failed to fetch headlines: {data.get('message', 'Unknown error')}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch headlines: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def search_news(self, query: str, language: str = 'en', sort_by: str = 'publishedAt', page_size: int = 10) -> Dict:
        """
        Search for news articles
        
        Args:
            query: Search query
            language: Language code (e.g., 'en', 'es', 'fr')
            sort_by: Sort order (relevancy, popularity, publishedAt)
            page_size: Number of articles to return (max 100 for free tier)
        
        Returns:
            Dictionary containing search results
        """
        if not self.api_key:
            return {"error": "NewsAPI key not configured"}
        
        try:
            params = {
                'q': query,
                'language': language,
                'sortBy': sort_by,
                'pageSize': min(page_size, 100),
                'apiKey': self.api_key
            }
            
            url = f"{self.base_url}/everything"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'ok':
                return self._format_search_results(data)
            else:
                return {"error": f"Failed to search news: {data.get('message', 'Unknown error')}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to search news: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_news_by_category(self, category: str, country: str = 'us', page_size: int = 10) -> Dict:
        """
        Get news by specific category
        
        Args:
            category: News category
            country: Country code
            page_size: Number of articles to return
        
        Returns:
            Dictionary containing category news
        """
        return self.get_top_headlines(country=country, category=category, page_size=page_size)
    
    def get_available_categories(self) -> List[str]:
        """Get list of available news categories"""
        return [
            'business',
            'entertainment', 
            'general',
            'health',
            'science',
            'sports',
            'technology'
        ]
    
    def get_available_countries(self) -> Dict[str, str]:
        """Get list of available country codes and names"""
        return {
            'ae': 'United Arab Emirates',
            'ar': 'Argentina',
            'at': 'Austria',
            'au': 'Australia',
            'be': 'Belgium',
            'bg': 'Bulgaria',
            'br': 'Brazil',
            'ca': 'Canada',
            'ch': 'Switzerland',
            'cn': 'China',
            'co': 'Colombia',
            'cu': 'Cuba',
            'cz': 'Czech Republic',
            'de': 'Germany',
            'eg': 'Egypt',
            'fr': 'France',
            'gb': 'United Kingdom',
            'gr': 'Greece',
            'hk': 'Hong Kong',
            'hu': 'Hungary',
            'id': 'Indonesia',
            'ie': 'Ireland',
            'il': 'Israel',
            'in': 'India',
            'it': 'Italy',
            'jp': 'Japan',
            'kr': 'South Korea',
            'lt': 'Lithuania',
            'lv': 'Latvia',
            'ma': 'Morocco',
            'mx': 'Mexico',
            'my': 'Malaysia',
            'ng': 'Nigeria',
            'nl': 'Netherlands',
            'no': 'Norway',
            'nz': 'New Zealand',
            'ph': 'Philippines',
            'pl': 'Poland',
            'pt': 'Portugal',
            'ro': 'Romania',
            'rs': 'Serbia',
            'ru': 'Russia',
            'sa': 'Saudi Arabia',
            'se': 'Sweden',
            'sg': 'Singapore',
            'si': 'Slovenia',
            'sk': 'Slovakia',
            'th': 'Thailand',
            'tr': 'Turkey',
            'tw': 'Taiwan',
            'ua': 'Ukraine',
            'us': 'United States',
            've': 'Venezuela',
            'za': 'South Africa'
        }
    
    def _format_headlines(self, data: Dict) -> Dict:
        """Format raw headlines data into a user-friendly format"""
        articles = []
        
        for article in data.get('articles', []):
            formatted_article = {
                "title": article.get('title'),
                "description": article.get('description'),
                "url": article.get('url'),
                "url_to_image": article.get('urlToImage'),
                "published_at": article.get('publishedAt'),
                "content": article.get('content'),
                "source": {
                    "id": article.get('source', {}).get('id'),
                    "name": article.get('source', {}).get('name')
                }
            }
            articles.append(formatted_article)
        
        return {
            "total_results": data.get('totalResults', 0),
            "articles": articles,
            "count": len(articles)
        }
    
    def _format_search_results(self, data: Dict) -> Dict:
        """Format raw search results into a user-friendly format"""
        return self._format_headlines(data)
