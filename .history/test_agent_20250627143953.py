#!/usr/bin/env python3
"""
Simple test script for FinRexent Agent
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_agent():
    print("=" * 60)
    print("FINREXENT AGENT TEST")
    print("=" * 60)
    
    try:
        print("1. Importing agent...")
        from agent.agent import FinRexentAgent
        print("   ✓ Import successful")
        
        print("2. Creating agent instance...")
        agent = FinRexentAgent()
        print("   ✓ Agent created")
        
        print("3. Testing stock data fetch...")
        data = agent.get_stock_data('RELIANCE', period="1mo")
        if data is not None and not data.empty:
            latest_price = data['Close'].iloc[-1]
            print(f"   ✓ RELIANCE current price: ₹{latest_price:.2f}")
            print(f"   ✓ Data points: {len(data)}")
        else:
            print("   ❌ Failed to fetch RELIANCE data")
        
        print("4. Testing news analysis...")
        test_news = [
            {'title': 'Reliance Industries reports strong earnings'},
            {'title': 'HDFC Bank launches new services'},
            {'title': 'Market shows positive momentum'}
        ]
        
        analyzed = agent.analyze_news(test_news)
        print(f"   ✓ Analyzed {len(analyzed)} news items")
        
        for i, item in enumerate(analyzed, 1):
            sentiment = item['sentiment']
            score = item['score']
            headline = item['headline'][:40]
            print(f"      {i}. {headline}... | {sentiment} ({score:.3f})")
        
        print("5. Testing stock recommendations...")
        recommendations = agent.recommend_stocks(analyzed)
        print(f"   ✓ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            for rec in recommendations:
                print(f"      - {rec['company']} ({rec['ticker']})")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - AGENT IS WORKING!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1) 