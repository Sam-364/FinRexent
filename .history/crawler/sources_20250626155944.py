"""
Data sources configuration for FinRexent crawler
"""
from typing import Dict, List, Any

# Indian Financial News Sources
INDIAN_NEWS_SOURCES = {
    'moneycontrol': {
        'name': 'Moneycontrol',
        'base_url': 'https://www.moneycontrol.com',
        'news_urls': [
            'https://www.moneycontrol.com/news/business/markets/',
            'https://www.moneycontrol.com/news/business/stocks/',
            'https://www.moneycontrol.com/news/business/economy/',
            'https://www.moneycontrol.com/news/business/companies/'
        ],
        'selectors': {
            'headlines': 'h2 a[title]',
            'content': '.article_content',
            'date': '.article_time',
            'author': '.author_name'
        }
    },
    'economic_times': {
        'name': 'Economic Times',
        'base_url': 'https://economictimes.indiatimes.com',
        'news_urls': [
            'https://economictimes.indiatimes.com/markets/stocks/news',
            'https://economictimes.indiatimes.com/markets/stocks/earnings',
            'https://economictimes.indiatimes.com/news/economy',
            'https://economictimes.indiatimes.com/news/company'
        ],
        'selectors': {
            'headlines': 'h3 a',
            'content': '.article_content',
            'date': '.publish_on',
            'author': '.author'
        }
    },
    'business_standard': {
        'name': 'Business Standard',
        'base_url': 'https://www.business-standard.com',
        'news_urls': [
            'https://www.business-standard.com/topic/markets',
            'https://www.business-standard.com/topic/stocks',
            'https://www.business-standard.com/topic/economy',
            'https://www.business-standard.com/topic/companies'
        ],
        'selectors': {
            'headlines': 'h2 a',
            'content': '.article-content',
            'date': '.date',
            'author': '.author'
        }
    },
    'livemint': {
        'name': 'Livemint',
        'base_url': 'https://www.livemint.com',
        'news_urls': [
            'https://www.livemint.com/market',
            'https://www.livemint.com/companies',
            'https://www.livemint.com/economy-policy',
            'https://www.livemint.com/industry'
        ],
        'selectors': {
            'headlines': 'h2 a',
            'content': '.article-content',
            'date': '.date',
            'author': '.author'
        }
    },
    'ndtv_profit': {
        'name': 'NDTV Profit',
        'base_url': 'https://www.ndtv.com/business',
        'news_urls': [
            'https://www.ndtv.com/business/market',
            'https://www.ndtv.com/business/stocks',
            'https://www.ndtv.com/business/economy',
            'https://www.ndtv.com/business/companies'
        ],
        'selectors': {
            'headlines': 'h2 a',
            'content': '.content_text',
            'date': '.posted_on',
            'author': '.author'
        }
    }
}

# Stock Market Data Sources
STOCK_DATA_SOURCES = {
    'nse': {
        'name': 'National Stock Exchange',
        'base_url': 'https://www.nseindia.com',
        'api_endpoints': {
            'live_data': '/api/quote-equity',
            'historical_data': '/api/historical/cm/equity',
            'company_info': '/api/quote-equity'
        }
    },
    'bse': {
        'name': 'Bombay Stock Exchange',
        'base_url': 'https://www.bseindia.com',
        'api_endpoints': {
            'live_data': '/api/quote',
            'historical_data': '/api/historical',
            'company_info': '/api/company'
        }
    },
    'yahoo_finance': {
        'name': 'Yahoo Finance',
        'base_url': 'https://finance.yahoo.com',
        'suffix': '.NS'  # NSE suffix for Indian stocks
    }
}

# Technical Analysis Data Sources
TECHNICAL_ANALYSIS_SOURCES = {
    'tradingview': {
        'name': 'TradingView',
        'base_url': 'https://www.tradingview.com',
        'endpoints': {
            'screener': '/screener/',
            'chart': '/chart/',
            'analysis': '/analysis/'
        }
    },
    'investing': {
        'name': 'Investing.com',
        'base_url': 'https://in.investing.com',
        'endpoints': {
            'technical_analysis': '/technical-analysis',
            'fundamental_analysis': '/fundamental-analysis'
        }
    }
}

# Economic Data Sources
ECONOMIC_DATA_SOURCES = {
    'rbi': {
        'name': 'Reserve Bank of India',
        'base_url': 'https://www.rbi.org.in',
        'endpoints': {
            'repo_rate': '/api/rates',
            'inflation': '/api/inflation',
            'forex': '/api/forex'
        }
    },
    'nse_indices': {
        'name': 'NSE Indices',
        'base_url': 'https://www.nseindia.com',
        'endpoints': {
            'nifty_50': '/api/indices',
            'bank_nifty': '/api/indices',
            'sensex': '/api/indices'
        }
    }
}

# Company Information Sources
COMPANY_INFO_SOURCES = {
    'moneycontrol_company': {
        'name': 'Moneycontrol Company Info',
        'base_url': 'https://www.moneycontrol.com/india/stockpricequote',
        'url_pattern': '/{company_name}/{company_name}'
    },
    'screener': {
        'name': 'Screener.in',
        'base_url': 'https://www.screener.in',
        'url_pattern': '/company/{company_name}/'
    },
    'tickertape': {
        'name': 'Tickertape',
        'base_url': 'https://www.tickertape.in',
        'url_pattern': '/stocks/{company_name}'
    }
}

# RSS Feeds for News
RSS_FEEDS = {
    'moneycontrol_rss': 'https://www.moneycontrol.com/rss/markets.xml',
    'economic_times_rss': 'https://economictimes.indiatimes.com/rssfeedstopstories.cms',
    'business_standard_rss': 'https://www.business-standard.com/rss/feed.rss',
    'livemint_rss': 'https://www.livemint.com/rss/feed.xml'
}

# API Keys Configuration
API_KEYS = {
    'alpha_vantage': 'YOUR_ALPHA_VANTAGE_API_KEY',
    'news_api': 'YOUR_NEWS_API_KEY',
    'firecrawl': 'YOUR_FIRECRAWL_API_KEY',
    'quandl': 'YOUR_QUANDL_API_KEY'
}

# Crawling Configuration
CRAWLING_CONFIG = {
    'max_articles_per_source': 50,
    'crawl_interval': 3600,  # 1 hour
    'request_delay': 1,  # seconds between requests
    'timeout': 30,
    'max_retries': 3,
    'user_agent': 'FinRexent/1.0 (Financial News Crawler)',
    'respect_robots_txt': True
}

# Content Filtering Keywords
FINANCIAL_KEYWORDS = [
    'stock', 'market', 'investment', 'trading', 'earnings', 'profit', 'loss',
    'revenue', 'growth', 'dividend', 'IPO', 'FPO', 'merger', 'acquisition',
    'quarterly results', 'annual report', 'financial results', 'market cap',
    'PE ratio', 'book value', 'ROE', 'ROCE', 'debt', 'equity', 'mutual fund',
    'portfolio', 'risk', 'volatility', 'beta', 'alpha', 'sharpe ratio'
]

# Indian Stock Market Keywords
INDIAN_MARKET_KEYWORDS = [
    'NSE', 'BSE', 'Nifty', 'Sensex', 'Bank Nifty', 'Nifty 50', 'Nifty 500',
    'Mid Cap', 'Small Cap', 'Large Cap', 'FII', 'DII', 'FPI', 'SEBI',
    'RBI', 'Repo Rate', 'CRR', 'SLR', 'GST', 'Demonetization', 'Make in India'
]

# Sector Keywords
SECTOR_KEYWORDS = {
    'banking': ['bank', 'financial', 'lending', 'credit', 'loan', 'deposit'],
    'technology': ['tech', 'software', 'IT', 'digital', 'cloud', 'AI', 'ML'],
    'pharmaceuticals': ['pharma', 'drug', 'medicine', 'healthcare', 'biotech'],
    'automobile': ['auto', 'car', 'vehicle', 'motor', 'transport'],
    'energy': ['oil', 'gas', 'power', 'energy', 'petroleum', 'renewable'],
    'real_estate': ['real estate', 'property', 'construction', 'housing'],
    'consumer_goods': ['FMCG', 'consumer', 'retail', 'fast moving'],
    'telecom': ['telecom', 'communication', 'mobile', 'internet', '5G']
}

def get_all_news_urls() -> List[str]:
    """Get all news URLs from configured sources"""
    urls = []
    for source in INDIAN_NEWS_SOURCES.values():
        urls.extend(source['news_urls'])
    return urls

def get_source_by_name(name: str) -> Dict[str, Any]:
    """Get source configuration by name"""
    for source in INDIAN_NEWS_SOURCES.values():
        if source['name'].lower() == name.lower():
            return source
    return {}

def get_rss_feeds() -> List[str]:
    """Get all RSS feed URLs"""
    return list(RSS_FEEDS.values())

def get_api_endpoints(source: str) -> Dict[str, str]:
    """Get API endpoints for a specific source"""
    return STOCK_DATA_SOURCES.get(source, {}).get('api_endpoints', {}) 