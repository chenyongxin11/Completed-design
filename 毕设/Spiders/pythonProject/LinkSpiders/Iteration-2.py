import pandas as pd
import requests
from bs4 import BeautifulSoup

# 读取Excel文件中的数据
def read_data_from_excel(filename):
    df = pd.read_excel(filename)
    return df

# 根据链接爬取页面的锚文本及其链接数据，并仅爬取类为"mw-page-container"及其子标签，忽略带有CSS类为"new"的标签
def crawl_page_data(url):
    anchor_texts = []
    link_urls = []
    try:
        print("Crawling page:", url)
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # 提取链接
            page_content = soup.find(class_='mw-parser-output')
            if page_content:
                for link in page_content.find_all('a', href=True, class_=lambda x: x != 'new'):
                    anchor_texts.append(link.text.strip())
                    # 如果链接以/wiki/开头，则添加前缀
                    if link['href'].startswith('/wiki/'):
                        link_urls.append('https://zh.wikipedia.org' + link['href'])
                    else:
                        link_urls.append(link['href'])
                    print("Anchor Text:", link.text.strip())  # 打印锚文本
                    print("Link URL:", link_urls[-1])  # 打印链接
    except Exception as e:
        print("Error crawling page:", url)
        print(e)
    return anchor_texts, link_urls

# 合并数据并保存至新的Excel文件
def merge_and_save_data(original_df, crawled_df, output_filename='link.xlsx'):
    merged_df = pd.concat([original_df, crawled_df]).reset_index(drop=True)
    merged_df.to_excel(output_filename, index=False)
    print(f"Merged data saved to {output_filename}")

# 示例用法
if __name__ == "__main__":
    # 读取原始数据
    original_df = read_data_from_excel('Result-Anchor-1.xlsx')

    # 爬取页面数据并合并
    crawled_anchor_texts = []
    crawled_link_urls = []
    for url in original_df['Link URL']:
        anchor_texts, link_urls = crawl_page_data(url)
        crawled_anchor_texts.extend(anchor_texts)
        crawled_link_urls.extend(link_urls)
    crawled_df = pd.DataFrame({'Anchor Text': crawled_anchor_texts, 'Link URL': crawled_link_urls})

    # 合并数据并保存至新的Excel文件
    merge_and_save_data(original_df, crawled_df)
