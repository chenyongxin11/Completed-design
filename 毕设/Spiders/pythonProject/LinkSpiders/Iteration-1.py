import requests
from bs4 import BeautifulSoup
import pandas as pd

class WikipediaAnchorCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.results = {'Anchor Text': [], 'Link URL': []}

    def crawl(self):
        self._crawl_page(self.start_url)

    def _crawl_page(self, url):
        print("Crawling:", url)

        try:
            response = requests.get(url)
            response.encoding = 'utf-8'  # 设置响应的字符编码为utf-8
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                print(soup)
                self._process_page(soup) # 打印当前爬取页面的标题

                # Find all links on the page and process them
                links = soup.find_all('a', href=True, class_=lambda x: x != 'new')  # 忽略css类为"new"的a标签
                for link in links:
                    anchor_text = link.text.strip()
                    link_url = link['href']
                    if self._is_valid_link(link_url):
                        if link_url.startswith('/wiki/'):
                            link_url = 'https://zh.wikipedia.org' + link_url
                        self.results['Anchor Text'].append(anchor_text)
                        self.results['Link URL'].append(link_url)
        except Exception as e:
            print("Error crawling page:", url)
            print(e)

    def _is_valid_link(self, url):
        return url.startswith('/wiki/') and ':' not in url

    def _process_page(self, soup):
        # Example: Extract title
        title = soup.find('h1', id='firstHeading').text
        print("Title:", title)

    def save_to_excel(self, filename='wiki_links.xlsx'):
        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False)
        print(f"Results saved to {filename}")

# Example usage:
if __name__ == "__main__":
    start_url = 'https://zh.wikipedia.org/wiki/%E5%8C%96%E5%AD%B8'  # 指定要爬取的页面
    crawler = WikipediaAnchorCrawler(start_url)
    crawler.crawl()
    crawler.save_to_excel()