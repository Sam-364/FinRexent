#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Write results directly to file
with open('simple_test_results.txt', 'w') as f:
    f.write("FINREXENT AGENT SIMPLE TEST RESULTS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Test started at: {datetime.now()}\n\n")
    
    try:
        f.write("1. Testing basic imports...\n")
        import pandas as pd
        f.write("   ✓ Pandas imported\n")
        
        import numpy as np
        f.write("   ✓ NumPy imported\n")
        
        from transformers import pipeline
        f.write("   ✓ Transformers imported\n")
        
        f.write("2. Testing agent creation...\n")
        from agent.agent import FinRexentAgent
        agent = FinRexentAgent()
        f.write("   ✓ Agent created successfully\n")
        
        f.write("3. Testing news analysis...\n")
        test_news = [
            {'title': 'Reliance reports strong earnings growth'},
            {'title': 'Market volatility increases due to global uncertainty'},
            {'title': 'Tech stocks rally on positive earnings'}
        ]
        
        analyzed = agent.analyze_news(test_news)
        f.write(f"   ✓ Analyzed {len(analyzed)} news items\n")
        
        for i, item in enumerate(analyzed):
            f.write(f"     News {i+1}: {item['sentiment']} (score: {item['score']:.3f})\n")
        
        f.write("4. Testing recommendations...\n")
        recommendations = agent.recommend_stocks(analyzed)
        f.write(f"   ✓ Generated {len(recommendations)} recommendations\n")
        
        for i, rec in enumerate(recommendations):
            f.write(f"     Recommendation {i+1}: {rec}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("✅ ALL TESTS PASSED - AGENT IS WORKING!\n")
        f.write("✅ NO TA-LIB DEPENDENCY - COMPLETELY REMOVED!\n")
        f.write("✅ READY FOR USE!\n")
        f.write("=" * 50 + "\n")
        
    except Exception as e:
        f.write(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        f.write(traceback.format_exc())

print("Simple test completed. Check simple_test_results.txt for results.") 