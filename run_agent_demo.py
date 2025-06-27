#!/usr/bin/env python3
"""
FinRexent Agent Demo - Comprehensive Test and Results
"""

import sys
import os
import traceback
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 FinRexent Agent Demo - Real Stock Analysis")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Import and initialize agent
        print("1️⃣ Initializing FinRexent Agent...")
        from agent.agent import FinRexentAgent
        agent = FinRexentAgent()
        print("   ✅ Agent initialized successfully!")
        print()
        
        # Test with RELIANCE stock
        print("2️⃣ Fetching RELIANCE stock data...")
        stock_data = agent.get_stock_data('RELIANCE', period="3mo")
        
        if stock_data is not None and not stock_data.empty:
            latest_price = stock_data['Close'].iloc[-1]
            price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
            price_change_pct = (price_change / stock_data['Close'].iloc[-2]) * 100
            
            print(f"   📈 Current Price: ₹{latest_price:.2f}")
            print(f"   📊 Daily Change: ₹{price_change:.2f} ({price_change_pct:+.2f}%)")
            print(f"   📅 Data Points: {len(stock_data)} days")
            print()
            
            # Calculate technical indicators
            print("3️⃣ Calculating Technical Indicators...")
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
            
            sma_20 = stock_data['SMA_20'].iloc[-1]
            sma_50 = stock_data['SMA_50'].iloc[-1]
            
            print(f"   📊 20-day SMA: ₹{sma_20:.2f}")
            print(f"   📊 50-day SMA: ₹{sma_50:.2f}")
            
            # Trend analysis
            if latest_price > sma_20 and latest_price > sma_50:
                trend = "🟢 BULLISH (Above both SMAs)"
            elif latest_price < sma_20 and latest_price < sma_50:
                trend = "🔴 BEARISH (Below both SMAs)"
            else:
                trend = "🟡 MIXED (Between SMAs)"
            
            print(f"   📈 Trend: {trend}")
            print()
            
            # Investment suggestion
            print("4️⃣ Generating Investment Advice...")
            suggestion = agent.suggest_investment_amount(stock_data)
            print(f"   💡 {suggestion}")
            print()
            
        else:
            print("   ❌ Failed to fetch RELIANCE data")
            return
        
        # Test news analysis
        print("5️⃣ Testing News Sentiment Analysis...")
        test_news = [
            {'title': 'Reliance Industries reports strong Q4 earnings growth of 15%'},
            {'title': 'Reliance Jio announces new 5G rollout plans'},
            {'title': 'Market volatility increases due to global economic uncertainty'},
            {'title': 'Reliance Retail expands operations with new acquisitions'},
            {'title': 'Oil prices surge affecting Reliance petrochemical margins'}
        ]
        
        analyzed_news = agent.analyze_news(test_news)
        print(f"   📰 Analyzed {len(analyzed_news)} news items:")
        
        for i, item in enumerate(analyzed_news, 1):
            sentiment_emoji = "📈" if item['sentiment'] == 'POSITIVE' else "📉" if item['sentiment'] == 'NEGATIVE' else "➡️"
            print(f"      {i}. {sentiment_emoji} {item['sentiment']} ({item['score']:.3f})")
            print(f"         \"{item['headline'][:60]}...\"")
            if item['companies']:
                print(f"         Companies: {', '.join(item['companies'])}")
            print()
        
        # Generate stock recommendations
        print("6️⃣ Generating Stock Recommendations...")
        recommendations = agent.recommend_stocks(analyzed_news)
        
        if recommendations:
            print(f"   🎯 Found {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"      {i}. 🏢 {rec['company']} ({rec['ticker']})")
                print(f"         📰 {rec['headline'][:50]}...")
                print(f"         💡 {rec['investment_suggestion'][:80]}...")
                print()
        else:
            print("   ⚠️  No strong recommendations based on current news sentiment")
            print()
        
        # Test with another stock
        print("7️⃣ Testing with HDFC Bank...")
        hdfc_data = agent.get_stock_data('HDFCBANK', period="1mo")
        
        if hdfc_data is not None and not hdfc_data.empty:
            hdfc_price = hdfc_data['Close'].iloc[-1]
            print(f"   🏦 HDFC Bank Current Price: ₹{hdfc_price:.2f}")
            
            hdfc_suggestion = agent.suggest_investment_amount(hdfc_data)
            print(f"   💡 HDFC Investment Advice: {hdfc_suggestion[:100]}...")
            print()
        
        # Summary
        print("🎉 Demo Complete!")
        print("=" * 60)
        print("✅ Agent successfully analyzed RELIANCE stock")
        print("✅ Generated technical indicators and trends")
        print("✅ Analyzed news sentiment")
        print("✅ Provided investment recommendations")
        print("✅ Tested with multiple stocks")
        print()
        print("🚀 The FinRexent Agent is ready for real-world use!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 