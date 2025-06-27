#!/usr/bin/env python3
"""
FinRexent Agent Demo - Firecrawl Integration for Real Financial News Analysis
"""

import sys
import os
import traceback
from datetime import datetime
import getpass

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_firecrawl_api_key():
    """Get Firecrawl API key from user input"""
    print("🔑 Firecrawl API Key Required")
    print("=" * 50)
    print("To use advanced web scraping capabilities, you need a Firecrawl API key.")
    print("You can get one from: https://firecrawl.dev")
    print()
    
    while True:
        api_key = getpass.getpass("Enter your Firecrawl API key (or press Enter to skip): ").strip()
        
        if not api_key:
            print("⚠️  Skipping Firecrawl integration. Will use basic news sources.")
            return None
        
        if len(api_key) > 10:  # Basic validation
            print("✅ API key accepted!")
            return api_key
        else:
            print("❌ Invalid API key format. Please try again.")

def main():
    print("🚀 FinRexent Agent Demo - Advanced Financial News Analysis")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Get Firecrawl API key
        firecrawl_api_key = get_firecrawl_api_key()
        print()
        
        # Import and initialize agent
        print("1️⃣ Initializing FinRexent Agent...")
        from agent.agent import FinRexentAgent
        agent = FinRexentAgent()
        print("   ✅ Agent initialized successfully!")
        print()
        
        # Initialize crawler with Firecrawl if API key provided
        print("2️⃣ Initializing News Crawler...")
        if firecrawl_api_key:
            from crawler.crawler import StockNewsCrawler
            crawler = StockNewsCrawler(use_firecrawl=True, firecrawl_api_key=firecrawl_api_key)
            print("   ✅ Firecrawl-enabled crawler initialized!")
        else:
            from crawler.crawler import StockNewsCrawler
            crawler = StockNewsCrawler(use_firecrawl=False)
            print("   ✅ Basic crawler initialized!")
        print()
        
        # Crawl financial news
        print("3️⃣ Crawling Financial News...")
        if firecrawl_api_key:
            print("   🔥 Using Firecrawl for advanced web scraping...")
        else:
            print("   📰 Using basic RSS feeds and news sources...")
        
        news_articles = crawler.crawl_all_sources()
        
        if news_articles:
            print(f"   ✅ Successfully crawled {len(news_articles)} news articles")
            
            # Show sample of crawled news
            print("   📰 Sample headlines:")
            for i, article in enumerate(news_articles[:5], 1):
                title = article.get('title', article.get('headline', 'No title'))[:60]
                source = article.get('source', 'Unknown')
                print(f"      {i}. {title}... ({source})")
        else:
            print("   ⚠️  No news articles found, using sample data")
            news_articles = [
                {'title': 'Reliance Industries reports strong Q4 earnings growth of 15%', 'source': 'Sample'},
                {'title': 'HDFC Bank announces new digital banking initiatives', 'source': 'Sample'},
                {'title': 'Tata Motors launches new electric vehicle lineup', 'source': 'Sample'},
                {'title': 'Infosys signs major cloud computing contract', 'source': 'Sample'},
                {'title': 'Market volatility increases due to global economic uncertainty', 'source': 'Sample'}
            ]
        print()
        
        # Analyze news sentiment
        print("4️⃣ Analyzing News Sentiment...")
        analyzed_news = agent.analyze_news(news_articles)
        print(f"   ✅ Analyzed {len(analyzed_news)} news items")
        
        # Show sentiment analysis results
        positive_count = sum(1 for item in analyzed_news if item['sentiment'] == 'POSITIVE')
        negative_count = sum(1 for item in analyzed_news if item['sentiment'] == 'NEGATIVE')
        neutral_count = len(analyzed_news) - positive_count - negative_count
        
        print(f"   📊 Sentiment Distribution:")
        print(f"      📈 Positive: {positive_count} ({positive_count/len(analyzed_news)*100:.1f}%)")
        print(f"      📉 Negative: {negative_count} ({negative_count/len(analyzed_news)*100:.1f}%)")
        print(f"      ➡️  Neutral: {neutral_count} ({neutral_count/len(analyzed_news)*100:.1f}%)")
        print()
        
        # Generate stock recommendations
        print("5️⃣ Generating Stock Recommendations...")
        recommendations = agent.recommend_stocks(analyzed_news)
        
        if recommendations:
            print(f"   🎯 Found {len(recommendations)} strong recommendations:")
            print()
            
            for i, rec in enumerate(recommendations, 1):
                print(f"   📋 Recommendation #{i}")
                print(f"      🏢 Company: {rec['company']}")
                print(f"      📈 Ticker: {rec['ticker']}")
                print(f"      📰 News: {rec['headline'][:80]}...")
                print(f"      💡 Investment Advice: {rec['investment_suggestion']}")
                
                # Get current stock data for detailed analysis
                print(f"      📊 Fetching current stock data...")
                stock_data = agent.get_stock_data(rec['ticker'], period="3mo")
                
                if stock_data is not None and not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    prev_price = stock_data['Close'].iloc[-2]
                    price_change = current_price - prev_price
                    price_change_pct = (price_change / prev_price) * 100
                    
                    print(f"      💰 Current Price: ₹{current_price:.2f}")
                    print(f"      📈 Daily Change: ₹{price_change:.2f} ({price_change_pct:+.2f}%)")
                    
                    # Calculate technical indicators
                    stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
                    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
                    
                    sma_20 = stock_data['SMA_20'].iloc[-1]
                    sma_50 = stock_data['SMA_50'].iloc[-1]
                    
                    print(f"      📊 20-day SMA: ₹{sma_20:.2f}")
                    print(f"      📊 50-day SMA: ₹{sma_50:.2f}")
                    
                    # Trend analysis
                    if current_price > sma_20 and current_price > sma_50:
                        trend = "🟢 BULLISH"
                    elif current_price < sma_20 and current_price < sma_50:
                        trend = "🔴 BEARISH"
                    else:
                        trend = "🟡 MIXED"
                    
                    print(f"      📈 Technical Trend: {trend}")
                else:
                    print(f"      ❌ Could not fetch stock data for {rec['ticker']}")
                
                print()
        else:
            print("   ⚠️  No strong recommendations based on current news sentiment")
            print("   💡 This could be due to:")
            print("      - Low sentiment scores in news")
            print("      - No identifiable company names in news")
            print("      - Market uncertainty reflected in news")
            print()
        
        # Market overview
        print("6️⃣ Market Overview Analysis...")
        major_stocks = ['RELIANCE', 'HDFCBANK', 'TCS', 'INFY', 'ICICIBANK']
        
        print("   📊 Major Stock Analysis:")
        for ticker in major_stocks:
            stock_data = agent.get_stock_data(ticker, period="1mo")
            if stock_data is not None and not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                prev_price = stock_data['Close'].iloc[-5]  # 5 days ago
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                trend_emoji = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
                print(f"      {trend_emoji} {ticker}: ₹{current_price:.2f} ({change_pct:+.2f}% 5d)")
        
        print()
        
        # Summary and next steps
        print("🎉 Analysis Complete!")
        print("=" * 70)
        print("✅ Successfully crawled financial news")
        print("✅ Analyzed news sentiment")
        print("✅ Generated stock recommendations")
        print("✅ Provided technical analysis")
        print()
        
        if firecrawl_api_key:
            print("🔥 Firecrawl Integration Benefits:")
            print("   - Bypassed website authentication issues")
            print("   - Advanced content extraction")
            print("   - Better data quality and reliability")
            print("   - Access to premium financial news sources")
        else:
            print("💡 To unlock advanced features:")
            print("   - Get a Firecrawl API key from https://firecrawl.dev")
            print("   - Re-run this script with your API key")
        
        print()
        print("🚀 The FinRexent Agent is ready for real-world trading decisions!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 