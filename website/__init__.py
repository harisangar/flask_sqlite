from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
db = SQLAlchemy()
migrate = Migrate()

website = Blueprint('website', __name__, template_folder='templates', static_folder='static')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = 'secretkey'
    
    # Initialize database and migrations
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import views and register blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Register the website blueprint
    app.register_blueprint(website, url_prefix='')

    # Define the @before_first_request function to create tables and fetch weather data
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()  # Create tables based on models
    #     fetch_and_store_weather()  # Fetch weather data and store it in the database

    return app

def fetch_and_store_weather():
         
    import json
    from website.models import WeatherData
    import http.client

    # Weather API request setup
    conn_api = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }
    
    # Request weather data for a specific location
    conn_api.request("GET", "/current.json?q=53.1%2C-0.13", headers=headers)
    
    # Get the response and read the data
    res = conn_api.getresponse()
    data = res.read()
    weather_data = json.loads(data.decode("utf-8"))

    # Extract relevant information from the weather data
    location = weather_data['location']
    current = weather_data['current']
    condition = current['condition']

    # Create a new WeatherData instance
    

    existing_data = WeatherData.query.filter_by(
        name=location['name'],
        condition_code=condition['code']
    ).first()


    if existing_data is None:
        weather_info = WeatherData(
            name=location['name'],
            country=location['country'],
            temp_c=current['temp_c'],
            humidity=current['humidity'],
            wind_kph=current['wind_kph'],
            condition_text=current['condition']['text'],
            condition_icon=current['condition']['icon'],
            condition_code=current['condition']['code'],
            localtime=location['localtime']
        )
        db.session.add(weather_info)
        db.session.commit()
        print("Weather data inserted into PostgreSQL!")

    else:
        print("Weather data for this country and localtime already exists, skipping insert.")





def fetchcityeather(city_name):
         
    import json
    from website.models import WeatherData
    import http.client

    # Weather API request setup
    from urllib.parse import urlencode

# Set up the HTTP connection
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

# Set up the headers with your RapidAPI key
    headers = {
    'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    
    }
    current_url = "https://weatherapi-com.p.rapidapi.com/current.json"
    params =urlencode({"q": city_name})

# Make the request to fetch the weather data for a given latitude and longitude
    conn.request("GET", f"/current.json?{params}",headers=headers)
    
    # Get the response and read the data
    res = conn.getresponse()
    data = res.read()
    weather_data = json.loads(data.decode("utf-8"))

    # Extract relevant information from the weather data
    location = weather_data['location']
    current = weather_data['current']
    condition = current['condition']

    # Create a new WeatherData instance
    

    existing_data = WeatherData.query.filter_by(
        name=location['name'],
        condition_code=condition['code']
    ).first()


    if existing_data is None:
        weather_info = WeatherData(
            name=location['name'],
            country=location['country'],
            temp_c=current['temp_c'],
            humidity=current['humidity'],
            wind_kph=current['wind_kph'],
            condition_text=current['condition']['text'],
            condition_icon=current['condition']['icon'],
            condition_code=current['condition']['code'],
            localtime=location['localtime']
        )
        db.session.add(weather_info)
        db.session.commit()
        print("Weather data inserted into PostgreSQL!")

    else:
        print("Weather data for this country and localtime already exists, skipping insert.")


def fetchdashboarddata(city):
     import json
     from website.models import WeatherData
     city_weather = WeatherData.query.filter_by(name=city).first()
     if city_weather:
        # Initialize a dictionary to store the weather information
        weather_info = {}

        # If localtime is a string, convert it to a datetime object
        localtime = city_weather.localtime
        if isinstance(localtime, str):
            localtime = datetime.strptime(localtime, "%Y-%m-%d %H:%M:%S")

        # Extract the day of the week and date
        day_of_week = localtime.strftime("%A")  # Full day name (e.g., "Saturday")
        date = localtime.strftime("%Y-%m-%d")  # Date (e.g., "2024-12-26")

        # Store the relevant weather information in the dictionary
        weather_info = {
            "day_of_week": day_of_week,
            "date": date,
            "city": city_weather.name,
            "country": city_weather.country,
            "temperature": f"{city_weather.temp_c}°C",
            "humidity": f"{city_weather.humidity}%",
            "wind_speed": f"{city_weather.wind_kph} kph",
            "condition_text": city_weather.condition_text,
            "condition_icon": city_weather.condition_icon,
            "condition_code": city_weather.condition_code,
            "localtime": city_weather.localtime.strftime("%Y-%m-%d %H:%M:%S")  # Ensure it's formatted properly
        }

        return weather_info
    