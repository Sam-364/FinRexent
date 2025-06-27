from crawler.crawler import StockNewsCrawler
from agent.agent import FinRexentAgent
import pandas as pd

def main():
    print("=== FinRexent Financial Analysis Agent ===\n")
    
    # Initialize the crawler
    print("1. Initializing news crawler...")
    crawler = StockNewsCrawler()
    
    # Crawl news from all sources
    print("2. Crawling financial news...")
    try:
        news_headlines = crawler.crawl_all_sources()
        print(f"   ✓ Successfully crawled {len(news_headlines)} articles")
    except Exception as e:
        print(f"   ⚠ Warning: Crawler encountered issues: {e}")
        # Use dummy data if crawler fails
        news_headlines = [
            {'title': 'Reliance Industries reports strong Q4 earnings', 'source': 'Economic Times'},
            {'title': 'HDFC Bank announces new digital banking initiatives', 'source': 'Business Standard'},
            {'title': 'Nifty 50 reaches new all-time high', 'source': 'Moneycontrol'},
            {'title': 'Tata Motors launches new electric vehicle lineup', 'source': 'Livemint'},
            {'title': 'Infosys signs major cloud computing contract', 'source': 'Reuters'}
        ]
        print("   ✓ Using sample data for demonstration")

    if not news_headlines:
        print("   ⚠ No news headlines available. Using sample data.")
        news_headlines = [
            {'title': 'Reliance Industries reports strong Q4 earnings', 'source': 'Economic Times'},
            {'title': 'HDFC Bank announces new digital banking initiatives', 'source': 'Business Standard'},
            {'title': 'Nifty 50 reaches new all-time high', 'source': 'Moneycontrol'}
        ]

    # Initialize the agent
    print("\n3. Initializing AI agent...")
    agent = FinRexentAgent()

    # Analyze the crawled news
    print("4. Analyzing news sentiment...")
    analyzed_news = agent.analyze_news(news_headlines)
    
    print(f"\n=== News Analysis Results ({len(analyzed_news)} articles) ===")
    for i, item in enumerate(analyzed_news[:5], 1):  # Show first 5 articles
        sentiment_emoji = "📈" if item['sentiment'] == 'POSITIVE' else "📉" if item['sentiment'] == 'NEGATIVE' else "➡️"
        print(f"{i}. {sentiment_emoji} {item['headline'][:80]}...")
        print(f"   Sentiment: {item['sentiment']} (Score: {item['score']:.3f})")
        if item['companies']:
            print(f"   Companies: {', '.join(item['companies'])}")
        print()

    # Get stock recommendations
    print("5. Generating stock recommendations...")
    recommendations = agent.recommend_stocks(analyzed_news)
    
    if recommendations:
        print(f"\n=== Stock Recommendations ({len(recommendations)} found) ===")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. 🏢 {rec['company']} ({rec['ticker']})")
            print(f"   📰 News: {rec['headline'][:60]}...")
            print(f"   💡 Suggestion: {rec['investment_suggestion']}")
            print()
    else:
        print("\n⚠ No strong stock recommendations based on current news sentiment.")

    # Fetch and analyze specific stock data
    print("6. Fetching stock data for demonstration...")
    test_tickers = ['RELIANCE', 'HDFCBANK', 'TCS', 'INFY', 'TATAMOTORS']
    
    for ticker in test_tickers:
        print(f"\n--- {ticker} Stock Analysis ---")
        stock_data = agent.get_stock_data(ticker, period="6mo")
        
        if stock_data is not None and not stock_data.empty:
            latest_price = stock_data['Close'].iloc[-1]
            price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
            price_change_pct = (price_change / stock_data['Close'].iloc[-2]) * 100
            
            print(f"Current Price: ₹{latest_price:.2f}")
            print(f"Daily Change: ₹{price_change:.2f} ({price_change_pct:+.2f}%)")
            
            # Calculate technical indicators
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
            
            sma_20 = stock_data['SMA_20'].iloc[-1]
            sma_50 = stock_data['SMA_50'].iloc[-1]
            
            print(f"20-day SMA: ₹{sma_20:.2f}")
            print(f"50-day SMA: ₹{sma_50:.2f}")
            
            # Technical analysis
            if latest_price > sma_20 and latest_price > sma_50:
                trend = "🟢 Bullish (Above both SMAs)"
            elif latest_price < sma_20 and latest_price < sma_50:
                trend = "🔴 Bearish (Below both SMAs)"
            else:
                trend = "🟡 Mixed (Between SMAs)"
            
            print(f"Trend: {trend}")
            
            # Investment suggestion
            suggestion = agent.suggest_investment_amount(stock_data)
            print(f"Investment Advice: {suggestion}")
            
        else:
            print(f"❌ Unable to fetch data for {ticker}")

    # Store analysis in agent memory
    agent.add_to_memory({
        'query': 'comprehensive market analysis',
        'news_count': len(analyzed_news),
        'recommendations_count': len(recommendations),
        'timestamp': pd.Timestamp.now().isoformat()
    })

    print(f"\n=== Analysis Complete ===")
    print(f"📊 Articles analyzed: {len(analyzed_news)}")
    print(f"💼 Recommendations generated: {len(recommendations)}")
    print(f"🧠 Agent memory entries: {len(agent.get_memory())}")
    
    print("\n🎯 The agent is now ready for manual testing!")
    print("You can run: python3 -c \"from agent.agent import FinRexentAgent; agent = FinRexentAgent(); print(agent.get_stock_data('RELIANCE').tail())\"")

if __name__ == "__main__":
    main()
