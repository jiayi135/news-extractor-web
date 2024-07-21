from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import concurrent.futures

app = Flask(__name__)

def extract_news(url, site_name):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        news_items = []
        
        if site_name == "纽约时报":
            articles = soup.find_all('div', class_='story-body')
            for article in articles[:5]:
                title = article.find('h3', class_='article-title').text.strip() if article.find('h3', class_='article-title') else ''
                link = 'https://cn.nytimes.com' + article.find('a')['href'] if article.find('a') else ''
                news_items.append((title, link))
        
        # ... [其他网站的提取逻辑保持不变] ...
        
        return news_items
    except Exception as e:
        print(f"Error extracting news from {site_name}: {str(e)}")
        return []

@app.route('/')
def index():
    sites = {
        "纽约时报": "https://cn.nytimes.com/",
        "路透社": "https://cn.reuters.com/",
        "BBC": "https://www.bbc.com/zhongwen/simp",
        "美国之音": "https://www.voachinese.com/",
        "法广": "https://www.rfi.fr/cn/",
        "德国之声": "https://www.dw.com/zh/"
    }
    
    all_news = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_site = {executor.submit(extract_news, url, name): name for name, url in sites.items()}
        for future in concurrent.futures.as_completed(future_to_site):
            site_name = future_to_site[future]
            try:
                news_items = future.result()
                all_news[site_name] = news_items
            except Exception as exc:
                print(f'{site_name} generated an exception: {exc}')
    
    return render_template('index.html', all_news=all_news)

if __name__ == '__main__':
    app.run(debug=True)
