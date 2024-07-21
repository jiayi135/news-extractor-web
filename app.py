from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_news():
    # 示例新闻数据
    all_news = {
        "BBC": [
            ("Title 1", "https://example.com/news1", "https://example.com/image1.jpg", "Summary 1"),
            ("Title 2", "https://example.com/news2", "https://example.com/image2.jpg", "Summary 2"),
            # 其他新闻条目...
        ],
        "CNN": [
            ("Title A", "https://example.com/newsA", "https://example.com/imageA.jpg", "Summary A"),
            ("Title B", "https://example.com/newsB", "https://example.com/imageB.jpg", "Summary B"),
            # 其他新闻条目...
        ],
        # 其他新闻来源...
    }
    return all_news

@app.route('/')
def index():
    all_news = get_news()
    return render_template('index.html', all_news=all_news)

if __name__ == '__main__':
    app.run(debug=True)
