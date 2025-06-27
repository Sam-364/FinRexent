import requests
from bs4 import BeautifulSoup

class StockNewsCrawler:
    def __init__(self, sources):
        self.sources = sources

    def crawl(self):
        all_news = []
        for source in self.sources:
            try:
                response = requests.get(source['url'])
                soup = BeautifulSoup(response.content, 'html.parser')
                # Look for <a> tags within <h2> tags that have a 'title' attribute
                headlines = soup.find_all('h2')
                for h2_tag in headlines:
                    a_tag = h2_tag.find('a')
                    if a_tag and a_tag.has_attr('title'):
                        all_news.append({
                            'source': source['name'],
                            'headline': a_tag['title'].strip()
                        })
            except Exception as e:
                print(f"Error crawling {source['url']}: {e}")
        return all_news

if __name__ == '__main__':
    # Example usage:
    sources = [
        {
            'name': 'Moneycontrol',
            'url': 'https://www.moneycontrol.com/news/business/markets/',
        }
    ]
    crawler = StockNewsCrawler(sources)
    news = crawler.crawl()
    for item in news:
        print(f"[{item['source']}] {item['headline']}")