import os
import datetime
from flask import Flask, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.utils import redirect

from models.errors import CityError

app = Flask(__name__)
api_key = os.environ.get('API_KEY', None)
app.secret_key = os.environ.get('secret_key')

@app.route('/')
def index():
    return render_template('home.html')



@app.route('/current', methods=['GET', 'POST'])
def current():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
        r = requests.get(url.format(city, api_key)).json()
        # print(r)
        if r['cod'] == '404':
            flash('City not found')
            return redirect(url_for('current'))
        weather = {
            "city": city,
            "temperature": int(r['main']['temp']),
            "description": r['weather'][0]['description'],
            "pressure": int(r['main']['pressure']),
            "humidity": int(r['main']['humidity']),
            "icon": r['weather'][0]['icon']
        }

        # print(weather)

    return render_template('weather.html', weather=weather)


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}"
        r = requests.get(url.format(city, api_key)).json()
        if r['cod'] == '404':
            flash('City not found')
            return redirect(url_for('current'))
        cdate1 = str(datetime.datetime.utcfromtimestamp(r['list'][0]['dt']))
        date1 = cdate1[:10]
        cdate2 = str(datetime.datetime.utcfromtimestamp(r['list'][8]['dt']))
        date2 = cdate2[:10]
        cdate3 = str(datetime.datetime.utcfromtimestamp(r['list'][16]['dt']))
        date3 = cdate3[:10]

        weather = {
            "city": city,
            "date1": date1,
            "tem_min1": int(r['list'][0]['main']['temp_min']),
            "tem_max1": int(r['list'][0]['main']['temp_max']),
            "description1": r['list'][0]['weather'][0]['description'],
            "pressure1": int(r['list'][0]['main']['pressure']),
            "humidity1": int(r['list'][0]['main']['humidity']),
            "icon1": r['list'][0]['weather'][0]['icon'],
            "date2": date2,
            "tem_min2": int(r['list'][8]['main']['temp_min']),
            "tem_max2": int(r['list'][8]['main']['temp_max']),
            "description2": r['list'][8]['weather'][0]['description'],
            "pressure2": int(r['list'][8]['main']['pressure']),
            "humidity2": int(r['list'][8]['main']['humidity']),
            "icon2": r['list'][8]['weather'][0]['icon'],
            "date3": date3,
            "tem_min3": int(r['list'][16]['main']['temp_min']),
            "tem_max3": int(r['list'][16]['main']['temp_max']),
            "description3": r['list'][16]['weather'][0]['description'],
            "pressure3": int(r['list'][16]['main']['pressure']),
            "humidity3": int(r['list'][16]['main']['humidity']),
            "icon3": r['list'][16]['weather'][0]['icon']
        }

        print(weather)

    return render_template('forecast.html', weather=weather)

