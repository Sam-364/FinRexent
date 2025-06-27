"""
Firecrawl client for advanced web scraping
"""
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
from utils.logger import logger

class FirecrawlClient:
    """Client for Firecrawl web scraping service"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.firecrawl.dev"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def scrape_url(self, url: str, options: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Scrape a single URL"""
        try:
            payload = {
                'url': url,
                'options': options or {}
            }
            
            response = self.session.post(
                f"{self.base_url}/scrape",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Firecrawl API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {str(e)}")
            return None
    
    def scrape_urls(self, urls: List[str], options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Scrape multiple URLs"""
        results = []
        
        for url in urls:
            result = self.scrape_url(url, options)
            if result:
                results.append(result)
            
            # Rate limiting
            time.sleep(1)
        
        return results
    
    def extract_news_content(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract news content from scraped data"""
        if not scraped_data or 'data' not in scraped_data:
            return {}
        
        data = scraped_data['data']
        
        # Extract text content
        content = data.get('text', '')
        html = data.get('html', '')
        
        # Extract metadata
        metadata = {
            'title': data.get('metadata', {}).get('title', ''),
            'description': data.get('metadata', {}).get('description', ''),
            'author': data.get('metadata', {}).get('author', ''),
            'published_date': data.get('metadata', {}).get('publishedDate', ''),
            'url': data.get('url', ''),
            'scraped_at': datetime.now().isoformat()
        }
        
        return {
            'content': content,
            'html': html,
            'metadata': metadata,
            'url': data.get('url', '')
        }
    
    def extract_financial_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract financial data from scraped content"""
        content = scraped_data.get('content', '')
        metadata = scraped_data.get('metadata', {})
        
        # Extract potential stock tickers
        import re
        ticker_pattern = r'\b[A-Z]{2,5}\.NS\b'
        tickers = re.findall(ticker_pattern, content.upper())
        
        # Extract potential numbers (prices, percentages)
        price_pattern = r'₹\s*[\d,]+\.?\d*'
        prices = re.findall(price_pattern, content)
        
        percentage_pattern = r'[\d.]+%'
        percentages = re.findall(percentage_pattern, content)
        
        return {
            'tickers': list(set(tickers)),
            'prices': prices,
            'percentages': percentages,
            'title': metadata.get('title', ''),
            'url': metadata.get('url', ''),
            'published_date': metadata.get('published_date', '')
        }
    
    def is_valid_response(self, response: Dict[str, Any]) -> bool:
        """Check if the scraped response is valid"""
        if not response:
            return False
        
        if 'error' in response:
            return False
        
        if 'data' not in response:
            return False
        
        data = response['data']
        if not data.get('text') and not data.get('html'):
            return False
        
        return True

class NewsScraper:
    """Specialized news scraper using Firecrawl"""
    
    def __init__(self, firecrawl_client: FirecrawlClient):
        self.client = firecrawl_client
    
    def scrape_financial_news(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape financial news from multiple URLs"""
        options = {
            'wait_for': 2000,  # Wait 2 seconds for dynamic content
            'screenshot': False,
            'pdf': False,
            'metadata': True,
            'extract_rules': {
                'title': 'h1, h2, h3',
                'content': 'article, .content, .post-content',
                'date': 'time, .date, .published-date'
            }
        }
        
        scraped_data = self.client.scrape_urls(urls, options)
        news_articles = []
        
        for data in scraped_data:
            if self.client.is_valid_response(data):
                extracted = self.client.extract_news_content(data)
                financial_data = self.client.extract_financial_data(extracted)
                
                if extracted.get('content'):
                    news_articles.append({
                        'content': extracted['content'],
                        'title': extracted['metadata']['title'],
                        'url': extracted['url'],
                        'published_date': extracted['metadata']['published_date'],
                        'financial_data': financial_data
                    })
        
        return news_articles
    
    def scrape_stock_pages(self, tickers: List[str]) -> List[Dict[str, Any]]:
        """Scrape stock information pages"""
        # Common stock information URLs
        base_urls = [
            f"https://www.moneycontrol.com/india/stockpricequote/{ticker.lower()}/{ticker.lower()}"
            for ticker in tickers
        ]
        
        options = {
            'wait_for': 3000,
            'metadata': True,
            'extract_rules': {
                'price': '.pcp_price',
                'change': '.pcp_change',
                'volume': '.volume',
                'market_cap': '.market_cap'
            }
        }
        
        scraped_data = self.client.scrape_urls(base_urls, options)
        stock_data = []
        
        for data in scraped_data:
            if self.client.is_valid_response(data):
                extracted = self.client.extract_news_content(data)
                stock_data.append({
                    'url': extracted['url'],
                    'content': extracted['content'],
                    'metadata': extracted['metadata']
                })
        
        return stock_data 