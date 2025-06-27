from crawler.crawler import StockNewsCrawler
from agent.agent import FinRexentAgent

def main():
    # Initialize the crawler with Moneycontrol as a source
    sources = [
        {
            'name': 'Moneycontrol',
            'url': 'https://www.moneycontrol.com/news/business/markets/',
        }
    ]
    crawler = StockNewsCrawler()
    news_headlines = crawler.crawl_all_sources()

    if not news_headlines:
        print("No news headlines crawled. Exiting.")
        return

    # Initialize the agent
    agent = FinRexentAgent()

    # Analyze the crawled news
    analyzed_news = agent.analyze_news(news_headlines)
    print("\n--- Analyzed News Sentiment ---")
    for item in analyzed_news:
        print(f"Headline: {item['headline']}\nSentiment: {item['sentiment']} (Score: {item['score']:.4f})\n")

    # Recommend stocks based on positive sentiment news
    # NOTE: This part needs significant improvement for real-world use.
    # Currently, it just flags positive news. It doesn't link to specific stocks.
    # A more advanced NLP model for Named Entity Recognition (NER) would be needed
    # to extract company names from headlines and map them to stock tickers.
    recommendations = agent.recommend_stocks(analyzed_news)
    print("\n--- Stock Recommendations (Based on News Sentiment) ---")
    if recommendations:
        for rec in recommendations:
            print(f"Recommendation: {rec['headline']}\nReason: {rec['reason']}\n")
    else:
        print("No strong positive sentiment news for recommendations at this time.")

    # Example: Get stock data and suggest investment for a specific stock (e.g., Reliance)
    # In a real application, the agent would identify relevant stocks from news
    # and then fetch their data.
    print("\n--- Investment Suggestion for Reliance Industries (RELIANCE.NS) ---")
    reliance_data = agent.get_stock_data("RELIANCE")
    if reliance_data is not None:
        print("Latest Reliance Stock Data (last 5 days):\n", reliance_data.tail())
        investment_suggestion = agent.suggest_investment_amount(reliance_data)
        print("Investment Suggestion:", investment_suggestion)
    else:
        print("Could not fetch Reliance stock data.")

    # Add some data to agent's memory
    agent.add_to_memory({'news_analysis': analyzed_news})
    agent.add_to_memory({'reliance_data': reliance_data.to_dict() if reliance_data is not None else None})
    print("\n--- Agent Memory (Last two entries) ---")
    for entry in agent.get_memory()[-2:]:
        print(entry)

if __name__ == '__main__':
    main()
