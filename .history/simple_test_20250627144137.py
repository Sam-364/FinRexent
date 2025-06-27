#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Write to file directly
with open('test_results.txt', 'w') as f:
    f.write(f"=== FinRexent Test Started at {datetime.now()} ===\n")
    
    try:
        f.write("1. Testing imports...\n")
        import pandas as pd
        f.write("   ✓ Pandas imported\n")
        
        import yfinance as yf
        f.write("   ✓ YFinance imported\n")
        
        from transformers import pipeline
        f.write("   ✓ Transformers imported\n")
        
        f.write("2. Testing agent import...\n")
        from agent.agent import FinRexentAgent
        f.write("   ✓ Agent imported\n")
        
        f.write("3. Creating agent...\n")
        agent = FinRexentAgent()
        f.write("   ✓ Agent created\n")
        
        f.write("4. Testing stock data...\n")
        data = agent.get_stock_data('RELIANCE', period="1mo")
        if data is not None and not data.empty:
            latest_price = data['Close'].iloc[-1]
            f.write(f"   ✓ RELIANCE price: ₹{latest_price:.2f}\n")
            f.write(f"   ✓ Data points: {len(data)}\n")
        else:
            f.write("   ❌ No data for RELIANCE\n")
        
        f.write("5. Testing news analysis...\n")
        test_news = [{'title': 'Reliance reports strong earnings'}]
        analyzed = agent.analyze_news(test_news)
        f.write(f"   ✓ Analyzed {len(analyzed)} news items\n")
        
        for item in analyzed:
            f.write(f"      - {item['sentiment']} ({item['score']:.3f})\n")
        
        f.write("\n=== TEST COMPLETED SUCCESSFULLY ===\n")
        
    except Exception as e:
        f.write(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        f.write(traceback.format_exc())
    
    f.write(f"\n=== Test ended at {datetime.now()} ===\n")

print("Test completed. Check test_results.txt for output.") 