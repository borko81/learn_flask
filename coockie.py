import datetime

from flask import Flask, make_response, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    expr = datetime.datetime.now() + datetime.timedelta(days=1)
    response = make_response(render_template('cockie_html.html'))
    response.set_cookie("borko", "123Ala bala", expires=expr)
    return response


@app.route('/data')
def get_cookie():
    data = request.cookies.get('borko')
    return render_template('cockie_html.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
