from flask import Flask
import json
import requests

app = Flask(__name__)

URL = 'https://api.openweathermap.org/data/2.5/weather?q=Velingrad,bg&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'


@app.route('/')
def index():
    data = requests.get(URL)
    return {'CONTENT': data.json()['main']['temp_max']}


if __name__ == '__main__':
    app.run(debug=True)

