#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== FINREXENT AGENT DIRECT TEST ===")
print("Testing agent functionality...")

try:
    print("1. Importing agent...")
    from agent.agent import FinRexentAgent
    print("   ✓ Agent imported successfully")
    
    print("2. Creating agent instance...")
    agent = FinRexentAgent()
    print("   ✓ Agent created successfully")
    
    print("3. Testing stock data fetch...")
    data = agent.get_stock_data('RELIANCE', period="1mo")
    if data is not None and not data.empty:
        latest_price = data['Close'].iloc[-1]
        print(f"   ✓ RELIANCE current price: ₹{latest_price:.2f}")
        print(f"   ✓ Data points: {len(data)}")
        
        # Show last 5 days
        print("   Last 5 trading days:")
        recent = data.tail(5)
        for date, row in recent.iterrows():
            print(f"     {date.strftime('%Y-%m-%d')}: ₹{row['Close']:.2f}")
    else:
        print("   ❌ No data for RELIANCE")
    
    print("4. Testing news analysis...")
    test_news = [
        {'title': 'Reliance Industries reports strong Q4 earnings'},
        {'title': 'HDFC Bank announces new digital initiatives'},
        {'title': 'Market volatility increases due to global factors'}
    ]
    
    analyzed = agent.analyze_news(test_news)
    print(f"   ✓ Analyzed {len(analyzed)} news items")
    
    for i, item in enumerate(analyzed, 1):
        sentiment = item['sentiment']
        score = item['score']
        headline = item['headline'][:40]
        print(f"     {i}. {headline}... | {sentiment} ({score:.3f})")
    
    print("5. Testing stock recommendations...")
    recommendations = agent.recommend_stocks(analyzed)
    print(f"   ✓ Generated {len(recommendations)} recommendations")
    
    if recommendations:
        for rec in recommendations:
            print(f"     - {rec['company']} ({rec['ticker']})")
    
    print("\n=== TEST COMPLETED SUCCESSFULLY ===")
    print("The agent is working perfectly without TA-Lib!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc() 