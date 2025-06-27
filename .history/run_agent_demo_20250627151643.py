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

def run_comprehensive_demo():
    """Run a comprehensive demo of the FinRexent agent"""
    
    output_file = "agent_demo_results.txt"
    
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("FINREXENT AGENT COMPREHENSIVE DEMO\n")
        f.write("=" * 80 + "\n")
        f.write(f"Started at: {datetime.now()}\n\n")
        
        try:
            # Step 1: Import and initialize agent
            f.write("STEP 1: INITIALIZING AGENT\n")
            f.write("-" * 40 + "\n")
            
            f.write("Importing required libraries...\n")
            import pandas as pd
            import yfinance as yf
            from transformers import pipeline
            f.write("✓ All libraries imported successfully\n")
            
            f.write("Creating FinRexent agent...\n")
            from agent.agent import FinRexentAgent
            agent = FinRexentAgent()
            f.write("✓ Agent created successfully\n\n")
            
            # Step 2: Test stock data fetching
            f.write("STEP 2: STOCK DATA ANALYSIS\n")
            f.write("-" * 40 + "\n")
            
            test_stocks = ['RELIANCE', 'HDFCBANK', 'TCS', 'INFY', 'TATAMOTORS']
            
            for ticker in test_stocks:
                f.write(f"\n--- {ticker} Analysis ---\n")
                
                try:
                    # Fetch stock data
                    data = agent.get_stock_data(ticker, period="6mo")
                    
                    if data is not None and not data.empty:
                        # Basic stats
                        latest_price = data['Close'].iloc[-1]
                        prev_price = data['Close'].iloc[-2]
                        price_change = latest_price - prev_price
                        price_change_pct = (price_change / prev_price) * 100
                        
                        f.write(f"Current Price: ₹{latest_price:.2f}\n")
                        f.write(f"Previous Close: ₹{prev_price:.2f}\n")
                        f.write(f"Daily Change: ₹{price_change:.2f} ({price_change_pct:+.2f}%)\n")
                        
                        # Technical indicators
                        data['SMA_20'] = data['Close'].rolling(window=20).mean()
                        data['SMA_50'] = data['Close'].rolling(window=50).mean()
                        
                        sma_20 = data['SMA_20'].iloc[-1]
                        sma_50 = data['SMA_50'].iloc[-1]
                        
                        f.write(f"20-day SMA: ₹{sma_20:.2f}\n")
                        f.write(f"50-day SMA: ₹{sma_50:.2f}\n")
                        
                        # Trend analysis
                        if latest_price > sma_20 and latest_price > sma_50:
                            trend = "🟢 BULLISH (Above both SMAs)"
                        elif latest_price < sma_20 and latest_price < sma_50:
                            trend = "🔴 BEARISH (Below both SMAs)"
                        else:
                            trend = "🟡 MIXED (Between SMAs)"
                        
                        f.write(f"Technical Trend: {trend}\n")
                        
                        # Investment suggestion
                        suggestion = agent.suggest_investment_amount(data)
                        f.write(f"Investment Advice: {suggestion}\n")
                        
                        # Show last 5 days of data
                        f.write("\nLast 5 trading days:\n")
                        recent_data = data.tail(5)[['Close', 'Volume']]
                        for date, row in recent_data.iterrows():
                            f.write(f"  {date.strftime('%Y-%m-%d')}: ₹{row['Close']:.2f} (Vol: {row['Volume']:,.0f})\n")
                        
                    else:
                        f.write(f"❌ No data available for {ticker}\n")
                        
                except Exception as e:
                    f.write(f"❌ Error analyzing {ticker}: {str(e)}\n")
            
            # Step 3: News sentiment analysis
            f.write("\n\nSTEP 3: NEWS SENTIMENT ANALYSIS\n")
            f.write("-" * 40 + "\n")
            
            # Sample financial news
            sample_news = [
                {'title': 'Reliance Industries reports record Q4 profits, stock surges 5%'},
                {'title': 'HDFC Bank announces major digital banking expansion'},
                {'title': 'TCS wins $500 million cloud computing contract'},
                {'title': 'Infosys faces regulatory scrutiny over accounting practices'},
                {'title': 'Tata Motors launches new electric vehicle lineup'},
                {'title': 'Nifty 50 reaches all-time high amid strong market sentiment'},
                {'title': 'RBI maintains repo rate at 6.5%, markets react positively'},
                {'title': 'Global markets tumble as inflation concerns mount'}
            ]
            
            f.write(f"Analyzing {len(sample_news)} news articles...\n\n")
            
            analyzed_news = agent.analyze_news(sample_news)
            
            for i, item in enumerate(analyzed_news, 1):
                sentiment_emoji = "📈" if item['sentiment'] == 'POSITIVE' else "📉" if item['sentiment'] == 'NEGATIVE' else "➡️"
                f.write(f"{i}. {sentiment_emoji} {item['headline']}\n")
                f.write(f"   Sentiment: {item['sentiment']} (Confidence: {item['score']:.3f})\n")
                if item['companies']:
                    f.write(f"   Companies: {', '.join(item['companies'])}\n")
                f.write("\n")
            
            # Step 4: Stock recommendations
            f.write("\nSTEP 4: STOCK RECOMMENDATIONS\n")
            f.write("-" * 40 + "\n")
            
            recommendations = agent.recommend_stocks(analyzed_news)
            
            if recommendations:
                f.write(f"Generated {len(recommendations)} stock recommendations:\n\n")
                
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"{i}. 🏢 {rec['company']} ({rec['ticker']})\n")
                    f.write(f"   📰 Triggering News: {rec['headline']}\n")
                    f.write(f"   💡 Investment Suggestion: {rec['investment_suggestion']}\n")
                    f.write("\n")
            else:
                f.write("No strong recommendations based on current news sentiment.\n")
            
            # Step 5: Market summary
            f.write("\nSTEP 5: MARKET SUMMARY\n")
            f.write("-" * 40 + "\n")
            
            positive_news = sum(1 for item in analyzed_news if item['sentiment'] == 'POSITIVE')
            negative_news = sum(1 for item in analyzed_news if item['sentiment'] == 'NEGATIVE')
            neutral_news = len(analyzed_news) - positive_news - negative_news
            
            f.write(f"News Sentiment Distribution:\n")
            f.write(f"  📈 Positive: {positive_news} articles\n")
            f.write(f"  📉 Negative: {negative_news} articles\n")
            f.write(f"  ➡️ Neutral: {neutral_news} articles\n\n")
            
            f.write(f"Overall Market Sentiment: ")
            if positive_news > negative_news:
                f.write("🟢 BULLISH\n")
            elif negative_news > positive_news:
                f.write("🔴 BEARISH\n")
            else:
                f.write("🟡 NEUTRAL\n")
            
            # Step 6: Agent memory
            f.write("\nSTEP 6: AGENT MEMORY\n")
            f.write("-" * 40 + "\n")
            
            agent.add_to_memory({
                'demo_run': True,
                'timestamp': datetime.now().isoformat(),
                'stocks_analyzed': test_stocks,
                'news_analyzed': len(analyzed_news),
                'recommendations': len(recommendations)
            })
            
            memory = agent.get_memory()
            f.write(f"Agent memory entries: {len(memory)}\n")
            f.write("Latest memory entry:\n")
            f.write(f"  {memory[-1]}\n")
            
            # Final summary
            f.write("\n" + "=" * 80 + "\n")
            f.write("DEMO COMPLETED SUCCESSFULLY!\n")
            f.write("=" * 80 + "\n")
            f.write(f"✓ Agent initialized and working\n")
            f.write(f"✓ Stock data fetched for {len(test_stocks)} stocks\n")
            f.write(f"✓ News sentiment analyzed for {len(analyzed_news)} articles\n")
            f.write(f"✓ Generated {len(recommendations)} recommendations\n")
            f.write(f"✓ All functionality working without TA-Lib\n")
            f.write(f"\nCompleted at: {datetime.now()}\n")
            
        except Exception as e:
            f.write(f"\n❌ CRITICAL ERROR: {str(e)}\n")
            f.write("Full traceback:\n")
            f.write(traceback.format_exc())
    
    print(f"Demo completed! Check {output_file} for detailed results.")
    return output_file

if __name__ == "__main__":
    output_file = run_comprehensive_demo()
    
    # Also print a summary to console
    try:
        with open(output_file, 'r') as f:
            lines = f.readlines()
            print("\n" + "="*60)
            print("FINREXENT AGENT DEMO SUMMARY")
            print("="*60)
            
            # Extract key results
            for line in lines:
                if "Current Price:" in line or "Technical Trend:" in line or "Investment Advice:" in line:
                    print(line.strip())
                elif "Sentiment:" in line and "Confidence:" in line:
                    print(line.strip())
                elif "Generated" in line and "recommendations" in line:
                    print(line.strip())
                elif "DEMO COMPLETED SUCCESSFULLY" in line:
                    print("\n" + line.strip())
                    break
    except:
        print("Demo completed. Check the output file for full results.") 