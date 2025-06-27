"""
Enhanced Stock News Crawler for FinRexent
"""
import requests
import json
import time
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import feedparser
from pathlib import Path

from .firecrawl_client import FirecrawlClient, NewsScraper
from .sources import (
    INDIAN_NEWS_SOURCES, RSS_FEEDS, CRAWLING_CONFIG,
    FINANCIAL_KEYWORDS, INDIAN_MARKET_KEYWORDS
)
from utils.logger import logger
from utils.config import config

class StockNewsCrawler:
    """Enhanced stock news crawler with multiple sources and advanced features"""
    
    def __init__(self, use_firecrawl: bool = False, firecrawl_api_key: Optional[str] = None):
        self.sources = INDIAN_NEWS_SOURCES
        self.rss_feeds = RSS_FEEDS
        self.crawl_config = CRAWLING_CONFIG
        self.use_firecrawl = use_firecrawl
        
        # Initialize Firecrawl client if enabled
        if use_firecrawl and firecrawl_api_key:
            self.firecrawl_client = FirecrawlClient(firecrawl_api_key)
            self.news_scraper = NewsScraper(self.firecrawl_client)
        else:
            self.firecrawl_client = None
            self.news_scraper = None
        
        # Setup database for storing crawled data
        self.db_path = Path("data/news/crawled_news.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.crawl_config['user_agent']
        })
    
    def _init_database(self):
        """Initialize SQLite database for storing crawled news"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create news table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT UNIQUE,
                    source TEXT,
                    published_date TEXT,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sentiment_score REAL,
                    financial_keywords TEXT,
                    tickers TEXT,
                    processed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Create crawling history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crawl_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    url TEXT,
                    status TEXT,
                    articles_found INTEGER,
                    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def crawl_all_sources(self) -> List[Dict[str, Any]]:
        """Crawl all configured news sources with focus on RSS feeds"""
        all_news = []
        
        logger.info("Starting comprehensive news crawl")
        
        # Prioritize RSS feeds as they're more reliable
        logger.info("Crawling RSS feeds first...")
        rss_news = self._crawl_rss_feeds()
        all_news.extend(rss_news)
        logger.info(f"RSS feeds yielded {len(rss_news)} articles")
        
        # Try traditional news sources (with error handling)
        logger.info("Attempting to crawl traditional news sources...")
        for source_name, source_config in self.sources.items():
            try:
                logger.info(f"Crawling {source_config['name']}")
                news_from_source = self._crawl_source(source_name, source_config)
                all_news.extend(news_from_source)
                
                # Rate limiting
                time.sleep(self.crawl_config['request_delay'])
                
            except Exception as e:
                logger.warning(f"Skipping {source_name} due to error: {e}")
                continue
        
        # Use Firecrawl for advanced scraping if available
        if self.use_firecrawl and self.news_scraper:
            try:
                firecrawl_news = self._crawl_with_firecrawl()
                all_news.extend(firecrawl_news)
            except Exception as e:
                logger.warning(f"Firecrawl failed: {e}")
        
        # Filter and process news
        filtered_news = self._filter_financial_news(all_news)
        
        # Store in database
        if filtered_news:
            self._store_news(filtered_news)
        
        logger.info(f"Crawl completed. Found {len(filtered_news)} relevant articles")
        return filtered_news
    
    def _crawl_source(self, source_name: str, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Crawl a specific news source"""
        news_articles = []
        
        for url in source_config['news_urls']:
            try:
                response = self.session.get(url, timeout=self.crawl_config['timeout'])
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract headlines using configured selectors
                headlines = soup.select(source_config['selectors']['headlines'])
                
                for headline in headlines[:self.crawl_config['max_articles_per_source']]:
                    try:
                        article_url = headline.get('href')
                        if article_url and not article_url.startswith('http'):
                            article_url = source_config['base_url'] + article_url
                        
                        article_data = {
                            'title': headline.get('title', headline.get_text().strip()),
                            'url': article_url,
                            'source': source_config['name'],
                            'crawled_at': datetime.now().isoformat()
                        }
                        
                        # Try to extract additional content
                        if article_url:
                            article_content = self._extract_article_content(article_url, source_config)
                            article_data.update(article_content)
                        
                        news_articles.append(article_data)
                        
                    except Exception as e:
                        logger.warning(f"Error processing headline: {e}")
                        continue
                
                # Log crawl history
                self._log_crawl_history(source_name, url, 'success', len(headlines))
                
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
                self._log_crawl_history(source_name, url, 'error', 0)
        
        return news_articles
    
    def _extract_article_content(self, url: str, source_config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract article content from a specific URL"""
        try:
            response = self.session.get(url, timeout=self.crawl_config['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content = ""
            content_selectors = source_config['selectors'].get('content', '.content, .article-content, .post-content')
            
            for selector in content_selectors.split(', '):
                content_elements = soup.select(selector)
                if content_elements:
                    content = ' '.join([elem.get_text().strip() for elem in content_elements])
                    break
            
            # Extract date
            date = ""
            date_selectors = source_config['selectors'].get('date', '.date, .published-date, time')
            for selector in date_selectors.split(', '):
                date_elements = soup.select(selector)
                if date_elements:
                    date = date_elements[0].get_text().strip()
                    break
            
            # Extract author
            author = ""
            author_selectors = source_config['selectors'].get('author', '.author, .byline')
            for selector in author_selectors.split(', '):
                author_elements = soup.select(selector)
                if author_elements:
                    author = author_elements[0].get_text().strip()
                    break
            
            return {
                'content': content,
                'published_date': date,
                'author': author
            }
            
        except Exception as e:
            logger.warning(f"Error extracting content from {url}: {e}")
            return {}
    
    def _crawl_rss_feeds(self) -> List[Dict[str, Any]]:
        """Crawl RSS feeds for news"""
        rss_news = []
        
        for feed_name, feed_url in self.rss_feeds.items():
            try:
                logger.info(f"Crawling RSS feed: {feed_name}")
                
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:self.crawl_config['max_articles_per_source']]:
                    article_data = {
                        'title': entry.get('title', ''),
                        'content': entry.get('summary', ''),
                        'url': entry.get('link', ''),
                        'source': f"RSS_{feed_name}",
                        'published_date': entry.get('published', ''),
                        'crawled_at': datetime.now().isoformat()
                    }
                    
                    rss_news.append(article_data)
                
            except Exception as e:
                logger.error(f"Error crawling RSS feed {feed_name}: {e}")
        
        return rss_news
    
    def _crawl_with_firecrawl(self) -> List[Dict[str, Any]]:
        """Crawl using Firecrawl for advanced scraping"""
        if not self.news_scraper:
            return []
        
        try:
            # Get URLs from sources
            urls = []
            for source_config in self.sources.values():
                urls.extend(source_config['news_urls'][:5])  # Limit for API usage
            
            logger.info(f"Using Firecrawl to scrape {len(urls)} URLs")
            news_articles = self.news_scraper.scrape_financial_news(urls)
            
            return news_articles
            
        except Exception as e:
            logger.error(f"Error with Firecrawl scraping: {e}")
            return []
    
    def _filter_financial_news(self, news_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter news articles for financial relevance"""
        filtered_news = []
        
        for article in news_articles:
            title = article.get('title', '').lower()
            content = article.get('content', '').lower()
            
            # Check for financial keywords
            has_financial_keywords = any(keyword in title or keyword in content 
                                       for keyword in FINANCIAL_KEYWORDS)
            
            # Check for Indian market keywords
            has_indian_keywords = any(keyword.lower() in title or keyword.lower() in content 
                                    for keyword in INDIAN_MARKET_KEYWORDS)
            
            if has_financial_keywords or has_indian_keywords:
                # Extract tickers from content
                import re
                ticker_pattern = r'\b[A-Z]{2,5}\.NS\b'
                tickers = re.findall(ticker_pattern, content.upper())
                
                article['financial_keywords'] = [kw for kw in FINANCIAL_KEYWORDS 
                                               if kw in title or kw in content]
                article['tickers'] = list(set(tickers))
                article['relevance_score'] = len(article['financial_keywords']) + len(article['tickers'])
                
                filtered_news.append(article)
        
        # Sort by relevance score
        filtered_news.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return filtered_news
    
    def _store_news(self, news_articles: List[Dict[str, Any]]):
        """Store news articles in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for article in news_articles:
                cursor.execute('''
                    INSERT OR REPLACE INTO news_articles 
                    (title, content, url, source, published_date, crawled_at, 
                     financial_keywords, tickers, processed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article.get('title', ''),
                    article.get('content', ''),
                    article.get('url', ''),
                    article.get('source', ''),
                    article.get('published_date', ''),
                    article.get('crawled_at', ''),
                    json.dumps(article.get('financial_keywords', [])),
                    json.dumps(article.get('tickers', [])),
                    False
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored {len(news_articles)} articles in database")
            
        except Exception as e:
            logger.error(f"Error storing news in database: {e}")
    
    def _log_crawl_history(self, source: str, url: str, status: str, articles_found: int):
        """Log crawling history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO crawl_history (source, url, status, articles_found)
                VALUES (?, ?, ?, ?)
            ''', (source, url, status, articles_found))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging crawl history: {e}")
    
    def get_recent_news(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent news from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT title, content, url, source, published_date, 
                       financial_keywords, tickers, relevance_score
                FROM news_articles 
                WHERE crawled_at > ? AND processed = FALSE
                ORDER BY relevance_score DESC
            ''', (cutoff_time.isoformat(),))
            
            rows = cursor.fetchall()
            conn.close()
            
            news_articles = []
            for row in rows:
                news_articles.append({
                    'title': row[0],
                    'content': row[1],
                    'url': row[2],
                    'source': row[3],
                    'published_date': row[4],
                    'financial_keywords': json.loads(row[5]) if row[5] else [],
                    'tickers': json.loads(row[6]) if row[6] else [],
                    'relevance_score': row[7] or 0
                })
            
            return news_articles
            
        except Exception as e:
            logger.error(f"Error retrieving recent news: {e}")
            return []
    
    def get_news_by_ticker(self, ticker: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get news articles mentioning a specific ticker"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor.execute('''
                SELECT title, content, url, source, published_date, 
                       financial_keywords, tickers, relevance_score
                FROM news_articles 
                WHERE crawled_at > ? AND tickers LIKE ?
                ORDER BY relevance_score DESC
            ''', (cutoff_time.isoformat(), f'%{ticker}%'))
            
            rows = cursor.fetchall()
            conn.close()
            
            news_articles = []
            for row in rows:
                news_articles.append({
                    'title': row[0],
                    'content': row[1],
                    'url': row[2],
                    'source': row[3],
                    'published_date': row[4],
                    'financial_keywords': json.loads(row[5]) if row[5] else [],
                    'tickers': json.loads(row[6]) if row[6] else [],
                    'relevance_score': row[7] or 0
                })
            
            return news_articles
            
        except Exception as e:
            logger.error(f"Error retrieving news for ticker {ticker}: {e}")
            return []

if __name__ == '__main__':
    # Example usage
    crawler = StockNewsCrawler(use_firecrawl=False)
    news = crawler.crawl_all_sources()
    
    print(f"Crawled {len(news)} articles")
    for article in news[:5]:
        print(f"- {article['title']} ({article['source']})")
        print(f"  Tickers: {article.get('tickers', [])}")
        print(f"  Relevance: {article.get('relevance_score', 0)}")
        print()