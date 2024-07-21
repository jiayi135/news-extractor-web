import requests
from bs4 import BeautifulSoup

def get_bbc_news():
    url = "https://www.bbc.com/zhongwen/simp"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []
    
    for item in soup.select('.lx-stream-post__header-text'):
        title = item.get_text()
        link = item.find('a')['href']
        link = "https://www.bbc.com" + link if link.startswith('/') else link
        summary = item.find_next_sibling('p').get_text() if item.find_next_sibling('p') else ""
        news_items.append((title, link, summary, None))
    
    return news_items

def get_reuters_news():
    url = "https://cn.reuters.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []

    for item in soup.select('.story-content a'):
        title = item.get_text().strip()
        link = item['href']
        link = "https://cn.reuters.com" + link if link.startswith('/') else link
        summary = item.find_next_sibling('p').get_text().strip() if item.find_next_sibling('p') else ""
        news_items.append((title, link, summary, None))

    return news_items

def get_all_news():
    news = {
        "BBC 中文网": get_bbc_news(),
        "路透社中文网": get_reuters_news(),
        # 根据需要添加其他网站的提取函数
    }
    return news
