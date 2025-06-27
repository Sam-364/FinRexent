import pytest
from crawler.crawler import StockNewsCrawler
from crawler.sources import INDIAN_NEWS_SOURCES

@pytest.fixture
def crawler():
    return StockNewsCrawler(use_firecrawl=False)

def test_crawl_all_sources(crawler):
    news = crawler.crawl_all_sources()
    assert isinstance(news, list)
    if news:
        assert 'title' in news[0]
        assert 'url' in news[0]
        assert 'source' in news[0]

def test_filter_financial_news(crawler):
    # Simulate news articles
    articles = [
        {'title': 'Nifty surges 2% as Reliance rallies', 'content': 'Reliance Industries stock up on strong results', 'source': 'Moneycontrol'},
        {'title': 'Cricket World Cup', 'content': 'India wins', 'source': 'NDTV'},
    ]
    filtered = crawler._filter_financial_news(articles)
    assert any('Reliance' in art['title'] for art in filtered)
    assert all('financial_keywords' in art for art in filtered)

def test_recent_news(crawler):
    news = crawler.get_recent_news(hours=48)
    assert isinstance(news, list)
    if news:
        assert 'title' in news[0]
        assert 'relevance_score' in news[0] 