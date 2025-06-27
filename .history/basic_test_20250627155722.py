#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Write results directly to file
with open('basic_test_results.txt', 'w') as f:
    f.write("FINREXENT BASIC TEST RESULTS\n")
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
        
        f.write("2. Testing sentiment analysis...\n")
        # Create a simple sentiment analyzer
        sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        f.write("   ✓ Sentiment analyzer created\n")
        
        f.write("3. Testing news analysis...\n")
        test_news = [
            {'title': 'Reliance reports strong earnings growth'},
            {'title': 'Market volatility increases due to global uncertainty'},
            {'title': 'Tech stocks rally on positive earnings'}
        ]
        
        analyzed_news = []
        for news in test_news:
            result = sentiment_analyzer(news['title'])[0]
            analyzed_news.append({
                'title': news['title'],
                'sentiment': result['label'],
                'score': result['score']
            })
        
        f.write(f"   ✓ Analyzed {len(analyzed_news)} news items\n")
        
        for i, item in enumerate(analyzed_news):
            f.write(f"     News {i+1}: {item['sentiment']} (score: {item['score']:.3f})\n")
        
        f.write("4. Testing basic recommendations...\n")
        # Simple recommendation logic
        positive_news = [item for item in analyzed_news if item['sentiment'] == 'positive']
        negative_news = [item for item in analyzed_news if item['sentiment'] == 'negative']
        
        recommendations = []
        if positive_news:
            recommendations.append("Consider buying stocks with positive news sentiment")
        if negative_news:
            recommendations.append("Be cautious with stocks mentioned in negative news")
        
        f.write(f"   ✓ Generated {len(recommendations)} recommendations\n")
        
        for i, rec in enumerate(recommendations):
            f.write(f"     Recommendation {i+1}: {rec}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("✅ ALL BASIC TESTS PASSED!\n")
        f.write("✅ Core functionality working!\n")
        f.write("✅ Ready for development!\n")
        f.write("=" * 50 + "\n")
        
    except Exception as e:
        f.write(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        f.write(traceback.format_exc())

print("Basic test completed. Check basic_test_results.txt for results.") 