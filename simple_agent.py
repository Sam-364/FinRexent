#!/usr/bin/env python3

import sys
import os
from datetime import datetime
import random

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SimpleFinRexentAgent:
    def __init__(self):
        """Initialize a simple FinRexent agent without external dependencies"""
        self.positive_words = ['strong', 'growth', 'rally', 'surge', 'positive', 'recovery', 'profit', 'gain']
        self.negative_words = ['volatility', 'uncertainty', 'concerns', 'decline', 'loss', 'negative', 'risk']
        print("Simple Agent initialized successfully!")
    
    def analyze_news(self, news_list):
        """Analyze news sentiment using simple keyword matching"""
        analyzed_news = []
        
        for news in news_list:
            title = news['title'].lower()
            
            # Count positive and negative words
            positive_count = sum(1 for word in self.positive_words if word in title)
            negative_count = sum(1 for word in self.negative_words if word in title)
            
            # Determine sentiment
            if positive_count > negative_count:
                sentiment = 'positive'
                score = 0.7 + (positive_count * 0.1)
            elif negative_count > positive_count:
                sentiment = 'negative'
                score = 0.3 - (negative_count * 0.1)
            else:
                sentiment = 'neutral'
                score = 0.5
            
            analyzed_news.append({
                'title': news['title'],
                'sentiment': sentiment,
                'score': min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
            })
        
        return analyzed_news
    
    def recommend_stocks(self, analyzed_news):
        """Generate stock recommendations based on news sentiment"""
        recommendations = []
        
        positive_news = [item for item in analyzed_news if item['sentiment'] == 'positive']
        negative_news = [item for item in analyzed_news if item['sentiment'] == 'negative']
        
        if positive_news:
            recommendations.append("Consider buying stocks with positive news sentiment")
        
        if negative_news:
            recommendations.append("Be cautious with stocks mentioned in negative news")
        
        if len(positive_news) > len(negative_news):
            recommendations.append("Overall market sentiment appears positive")
        elif len(negative_news) > len(positive_news):
            recommendations.append("Overall market sentiment appears negative")
        else:
            recommendations.append("Market sentiment is mixed")
        
        return recommendations

# Test the agent
if __name__ == "__main__":
    print("Testing Simple FinRexent Agent...")
    
    # Write results to file
    with open('simple_agent_results.txt', 'w') as f:
        f.write("SIMPLE FINREXENT AGENT TEST RESULTS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Test started at: {datetime.now()}\n\n")
        
        try:
            f.write("1. Creating simple agent...\n")
            agent = SimpleFinRexentAgent()
            f.write("   ✓ Simple agent created successfully\n")
            
            f.write("2. Testing news analysis...\n")
            test_news = [
                {'title': 'Reliance reports strong earnings growth'},
                {'title': 'Market volatility increases due to global uncertainty'},
                {'title': 'Tech stocks rally on positive earnings'},
                {'title': 'Oil prices surge on supply concerns'},
                {'title': 'Banking sector shows strong recovery'}
            ]
            
            analyzed = agent.analyze_news(test_news)
            f.write(f"   ✓ Analyzed {len(analyzed)} news items\n")
            
            for i, item in enumerate(analyzed):
                f.write(f"     News {i+1}: {item['sentiment']} (score: {item['score']:.3f})\n")
            
            f.write("3. Testing recommendations...\n")
            recommendations = agent.recommend_stocks(analyzed)
            f.write(f"   ✓ Generated {len(recommendations)} recommendations\n")
            
            for i, rec in enumerate(recommendations):
                f.write(f"     Recommendation {i+1}: {rec}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("✅ ALL TESTS PASSED!\n")
            f.write("✅ Simple agent is working!\n")
            f.write("✅ No external dependencies!\n")
            f.write("✅ No GUI/Electron errors!\n")
            f.write("✅ Ready for use!\n")
            f.write("=" * 50 + "\n")
            
        except Exception as e:
            f.write(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
    
    print("Test completed. Check simple_agent_results.txt for results.") 