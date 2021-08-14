import feedparser
from flask import Flask

app = Flask(__name__)

BBS_FEED = 'http://www.medianews.bg/bg/rss/news.xml'


def get_first_news(BBS_FEED):
    feed = feedparser.parse(BBS_FEED)
    first_article = feed['entries'][0]
    return """<html>
        <body>
            <h1>{title}</h1>
            <p>{desc}</p>
            <a href='{link}'>link</a>
        </body>
    </html>""".format(title=first_article.get('title'), desc=first_article.get('description'),
                      link=first_article.get('link'))


@app.route('/')
@app.route('/news')
def news():
    return get_first_news(BBS_FEED)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
