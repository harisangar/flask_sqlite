from flask import Blueprint,render_template,request,flash,jsonify,json
from flask_login import  login_required,logout_user,current_user
# from .models import Note
from . import db
from . import fetch_and_store_weather,fetchcityeather
views = Blueprint('views',__name__)

@views.route('/',methods=['GET'])
# @login_required
def home():
    fetch_and_store_weather()

    # if request.method == 'POST':
    #     note=request.form.get('note')
    #     if len(note)<1:
    #         flash('note is too short ',category='error')
    #     else:
    #         new_note = Note(data=note,user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('note added ',category='success')



    return render_template("weather.html")


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