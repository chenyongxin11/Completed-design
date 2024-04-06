import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# 读取 Excel 文件中的链接数据
def read_links_from_excel(filename):
    df = pd.read_excel(filename)
    return df['Link URL']

# 爬取网页内容
def crawl_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # 提取标题
            title = soup.find(class_='mw-page-title-main').text.strip()
            print("Title:", title)
            # 提取内容
            content = ""
            content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')
            if content_div:
                paragraphs = content_div.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6'])
                for tag in paragraphs:
                    # 检查标签是否具有 style 属性，并且属性值包含 display:none
                    if tag.has_attr('style') and 'display:none' in tag['style']:
                        continue  # 忽略具有 style 属性为 display:none 的标签
                    if tag.name != 'p':
                        break
                    # 忽略 table 标签下的 p 标签
                    if tag.find_parents('table'):
                        continue
                    # 忽略 span 标签中 style 为 display:none 的内容
                    for span in tag.find_all('span', style=lambda x: x and 'display:none' in x):
                        span.decompose()  # 删除具有 style 为 display:none 的 span 标签
                    text = tag.text.strip()
                    # 删除 [1], [2], [3], ... 类型的文字
                    text = re.sub(r'\[\d+\]', '', text)
                    if text:
                        content += text + '\n'
            return title, url, content
    except Exception as e:
        print("Error crawling page:", url)
        print(e)
    return None, None, None

# 保存结果至 Excel 文件
def save_to_excel(results, output_filename='result.xlsx'):
    df = pd.DataFrame(results, columns=['Title', 'URL', 'Content'])
    df.to_excel(output_filename, index=False)
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    # 读取链接数据
    links = read_links_from_excel('LinkResult.xlsx')

    # 爬取内容
    results = []
    n = 1
    for link in links:
        print(n)
        n += 1
        print("Crawling page:", link)
        title, url, content = crawl_page_content(link)
        if title and url and content:
            results.append((title, url, content))

    # 保存结果至 Excel 文件
    save_to_excel(results)
