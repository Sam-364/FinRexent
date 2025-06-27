import yfinance as yf
from transformers import pipeline
import pandas as pd

class FinRexentAgent:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.memory = [] # Simple in-memory storage for now

    def analyze_news(self, news_headlines):
        analysis_results = []
        for news in news_headlines:
            # Handle both 'headline' and 'title' fields
            text = news.get('headline') or news.get('title', '')
            if not text:
                continue
                
            sentiment = self.sentiment_analyzer(text)[0]
            
            entities = self.ner_pipeline(text)
            company_names = self._reconstruct_company_names(entities)
            
            analysis_results.append({
                'headline': text,
                'sentiment': sentiment['label'],
                'score': sentiment['score'],
                'companies': list(set(company_names)) 
            })
        return analysis_results

    def _reconstruct_company_names(self, entities):
        reconstructed_names = []
        current_name = []
        for entity in entities:
            if entity['entity'].endswith('ORG'): 
                if entity['word'].startswith('##'):
                    current_name.append(entity['word'][2:])
                else:
                    if current_name:
                        reconstructed_names.append(" ".join(current_name))
                        current_name = []
                    current_name.append(entity['word'])
            else:
                if current_name:
                    reconstructed_names.append(" ".join(current_name))
                    current_name = []
        if current_name:
            reconstructed_names.append(" ".join(current_name))
        return reconstructed_names

    def get_stock_data(self, ticker, period="1y"):
        try:
            stock = yf.Ticker(ticker + ".NS") 
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def recommend_stocks(self, analyzed_news, market_trends=None):
        recommendations = []
        for news_item in analyzed_news:
            if news_item['sentiment'] == 'POSITIVE' and news_item['score'] > 0.9:
                for company in news_item['companies']:
                    ticker = self._get_ticker_from_company_name(company)
                    if ticker:
                        stock_data = self.get_stock_data(ticker)
                        if stock_data is not None and not stock_data.empty:
                            investment_suggestion = self.suggest_investment_amount(stock_data)
                            recommendations.append({
                                'company': company,
                                'ticker': ticker,
                                'headline': news_item['headline'],
                                'reason': f"Strong positive sentiment from news: {news_item['headline']}",
                                'investment_suggestion': investment_suggestion
                            })
        return recommendations

    def _get_ticker_from_company_name(self, company_name):
        # Hardcoded mapping for common Indian companies
        mapping = {
            "Reliance Industries": "RELIANCE",
            "HDFC Bank": "HDFCBANK",
            "Axis Bank": "AXISBANK",
            "Bharti Airtel": "BHARTIARTL",
            "Cummins India": "CUMMINSIND",
            "BPCL": "BPCL",
            "IOC": "IOC",
            "HPCL": "HINDPETRO",
            "SAIL": "SAIL",
            "Vedanta": "VEDL",
            "Tata Steel": "TATASTEEL",
            "Whirlpool": "WHIRLPOOL",
            "Voltas": "VOLTAS",
            "Coforge": "COFORGE",
            "IndiGo": "INDIGO",
            "Dr Reddy's": "DRREDDY",
            "Carraro India": "CARRAROIND",
            "Western Carriers": "WCL", 
            "Om Infra": "OMINFRAL",
            "FirstCry": "FIRSTCRY", # Added
            "Apar Industries": "APARINDS", # Added
            "Newgen Software": "NEWGEN", # Added
        }
        
        ticker = mapping.get(company_name)
        if ticker:
            return ticker

        # Attempt to find ticker using yfinance search
        try:
            # Try with .NS suffix first for Indian stocks
            ticker_info = yf.Ticker(company_name + ".NS").info
            if ticker_info and 'symbol' in ticker_info:
                return ticker_info['symbol'].replace(".NS", "")
        except Exception:
            pass # Ignore error and try without .NS

        try:
            # Try without .NS suffix
            ticker_info = yf.Ticker(company_name).info
            if ticker_info and 'symbol' in ticker_info:
                return ticker_info['symbol']
        except Exception:
            pass # Ignore error and return None
            
        return None

    def suggest_investment_amount(self, stock_data):
        if stock_data is None or stock_data.empty:
            return "Cannot suggest investment amount due to lack of data."

        stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()

        latest_close = stock_data['Close'].iloc[-1]
        sma_20 = stock_data['SMA_20'].iloc[-1]
        sma_50 = stock_data['SMA_50'].iloc[-1]

        stock_data['Daily_Return'] = stock_data['Close'].pct_change()
        volatility = stock_data['Daily_Return'].std() * (252**0.5) 

        suggestion = ""
        if latest_close > sma_20 and latest_close > sma_50:
            suggestion += "The stock shows a strong upward trend. "
            if volatility < 0.02: 
                suggestion += "Low volatility suggests a stable investment. Consider a higher investment."
            elif volatility < 0.05:
                suggestion += "Moderate volatility. Consider a moderate investment."
            else:
                suggestion += "High volatility. Exercise caution and consider a smaller investment."
        elif latest_close < sma_20 and latest_close < sma_50:
            suggestion += "The stock shows a downward trend. "
            if volatility > 0.05:
                suggestion += "High volatility in a downtrend suggests high risk. Avoid or consider very low investment."
            else:
                suggestion += "Lower volatility in a downtrend. Still, caution is advised. Consider low or no investment."
        else:
            suggestion += "The trend is mixed or uncertain. "
            if volatility > 0.05:
                suggestion += "High volatility in a mixed trend suggests high risk. Exercise extreme caution or avoid."
            else:
                suggestion += "Moderate to low volatility. Consider a cautious, small investment."
        
        return suggestion

    def add_to_memory(self, data):
        self.memory.append(data)

    def get_memory(self):
        return self.memory

if __name__ == '__main__':
    dummy_news = [
        {'source': 'Test', 'headline': 'Reliance Industries reports record profits, stock soars!'},
        {'source': 'Test', 'headline': 'HDFC Bank faces legal issues, shares plummet.'},
        {'source': 'Test', 'headline': 'Market remains stable amidst global uncertainties.'},
        {'source': 'Test', 'headline': 'Bharti Airtel launches new 5G services, stock gains.'},
    ]

    agent = FinRexentAgent()
    analyzed_news = agent.analyze_news(dummy_news)
    print("\nAnalyzed News with Companies:")
    for item in analyzed_news:
        print(item)

    recommendations = agent.recommend_stocks(analyzed_news)
    print("\nRecommendations:")
    if recommendations:
        for rec in recommendations:
            print(rec)
    else:
        print("No recommendations based on current news and criteria.")

    agent.add_to_memory({'query': 'dummy news analysis', 'result': analyzed_news})
    print("\nAgent Memory (Last entry):", agent.get_memory()[-1])
