import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    URL = 'https://api.openweathermap.org/data/2.5/weather?q=Velingrad,bg&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
    data = requests.get(URL)
    result = data.json()
    context = {
        'CONTENT': result['main']['temp_max'],
        'CITY': result['name']
    }
    return render_template('weather.html', context=context)


@app.route('/town_weather')
def town_weather():
    town_city = request.args.get('q')
    if not town_city:
        town_city = 'Velingrad'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={town_city},bg&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
    data = requests.get(URL)
    result = data.json()
    context = {
        'CONTENT': result['main']['temp_max'],
        'CITY': result['name']
    }
    return render_template('weather.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
