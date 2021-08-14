import feedparser
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

BBS_FEED = 'http://www.medianews.bg/bg/rss/news.xml'

check_name = {
    'name': 'First name',
    'age': '40',
    'email': 'korea60@abv.bg'
}


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


@app.route('/vesti')
@app.route('/news')
def news():
    return get_first_news(BBS_FEED)


@app.route('/')
def first_news():
    feed = feedparser.parse(BBS_FEED)
    first_article = feed['entries'][1]
    return render_template('news.html', context=first_article, one_new=1)


@app.route('/all')
def get_all_news():
    feed = feedparser.parse(BBS_FEED)
    query = request.args.get('title')
    result = [x for x in feed['entries'] if query.lower() in x.title.lower()]
    if query and result:
        return render_template('news.html', context=result)
    return render_template('news.html', context=feed['entries'])


@app.route('/search')
def from_check_name():
    query = request.args.get('search')
    if not query or query.lower() not in check_name:
        return 'Not found any data'
    return check_name[query]


if __name__ == '__main__':
    app.run(debug=True, port=5000)
