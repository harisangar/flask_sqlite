from flask import Blueprint,render_template,request,flash,jsonify,json
from flask_login import  login_required,logout_user,current_user
from website.models import WeatherData
from . import db
from . import fetch_and_store_weather,fetchcityeather,fetchdashboarddata
views = Blueprint('views',__name__)

@views.route('/',methods=['GET'])
# @login_required
def home():
    fetch_and_store_weather()
    jaffna_data=fetchdashboarddata("Jaffna")
    trinco_data=fetchdashboarddata("Trincomalee")
    vavuniya_data=fetchdashboarddata("Vavuniya")
    colombo_data=fetchdashboarddata("Colombo")

    city_names = db.session.query(WeatherData.name).distinct().all()

    # Convert the result into a list of city names
    city_names = [city[0] for city in city_names]

    # if request.method == 'POST':
    #     note=request.form.get('note')
    #     if len(note)<1:
    #         flash('note is too short ',category='error')
    #     else:
    #         new_note = Note(data=note,user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('note added ',category='success')



    return render_template("weather.html",jaffna_data=jaffna_data,vavuniya_data=vavuniya_data,colombo_data=colombo_data,trinco_data=trinco_data,city_names=city_names)


@views.route('/city', methods=['GET', 'POST'])
def fetchcity():
    city_name = request.args.get('name')  # or use 'city_name' based on your preference
    
    if not city_name:
        return jsonify({"error": "City name is required!"}), 400
    
    # Now you can call the function that fetches weather for the city
    fetchcityeather(city_name)
    return render_template("weather.html")
 
@views.route('/delete-note',methods=['POST'])
def delete_note():
    pass
    # note = json.loads(request.data)
    # noteId=note['noteId']
    # note = Note.query.get(noteId)
    # if note:
    #     if note.user_id == current_user.id:
    #         db.session.delete(note)
    #         db.session.commit()
    # return jsonify({})





@views.route('/add_city', methods=['POST'])
def fetch_city_weather():
    import http.client
    from urllib.parse import urlencode
    city_name = request.form.get('city_name')
    print('city name is'+city_name)

    if city_name:
        # Set up the HTTP connection
        conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': "4765efd0e4msh0e6f4310f441125p115acdjsnc5b407e62f78",
            'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
        }
        params = urlencode({"q": city_name})
        
        # Make the request to fetch the weather data for the city
        conn.request("GET", f"/current.json?{params}", headers=headers)
        
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
            return jsonify({"message": f"{city_name} city Weather data added succesfully"})
            

        else:
            return jsonify({"message": "Weather data already inserted!"})
        
        