from website import create_app




app = create_app()

if __name__ == "__main__":
    app.run(debug=True) 


 

# def fetch_and_store_weather():
#     # Make a request to the weather API
#     conn_api = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
#     headers = {
#         'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",
#         'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
#     }
#     conn_api.request("GET", "/current.json?q=53.1%2C-0.13", headers=headers)

#     # Get the response and read the data
#     res = conn_api.getresponse()
#     data = res.read()
#     weather_data = json.loads(data.decode("utf-8"))

#     # Extract relevant information
#     location = weather_data['location']
#     current = weather_data['current']

#     # Create a new WeatherData instance
#     weather_info = WeatherData(
#         name=location['name'],
#         country=location['country'],
#         temp_c=current['temp_c'],
#         humidity=current['humidity'],
#         wind_kph=current['wind_kph'],
#         condition_text=current['condition']['text'],
#         condition_icon=current['condition']['icon'],
#         condition_code=current['condition']['code']
#     )

#     # Add and commit to the database
#     db.session.add(weather_info)
#     db.session.commit()
#     print("Weather data inserted into PostgreSQL!")

# @app.before_first_request
# def create_tables():
#     db.create_all()  # Create tables in the database based on models
#     fetch_and_store_weather()  # Fetch data and store it after creating the tables


# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)