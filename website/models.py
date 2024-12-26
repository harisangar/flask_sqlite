# from . import db
# from flask_login import UserMixin
# from sqlalchemy import func

# class Note(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True),default=func.now())
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'))



# class User(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key=True)
#     email = db.Column(db.String(150),unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     notes = db.relationship('Note')

# from website import db
# from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<User {self.username}>"




from . import db
from datetime import datetime

class WeatherData(db.Model):
    __tablename__ = 'weather_data'  # Define the table name

    # Define columns
  
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    temp_c = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_kph = db.Column(db.Float, nullable=False)
    condition_text = db.Column(db.String(255), nullable=False)
    condition_icon = db.Column(db.String(255), nullable=False)
    condition_code = db.Column(db.Integer, nullable=False)
    localtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 


    __table_args__ = (
        db.PrimaryKeyConstraint('name', 'condition_code'),
    )

    def __repr__(self):
        return (f"<WeatherData {self.name}, {self.country}, {self.temp_c}°C, "
                f"Humidity: {self.humidity}%, Wind: {self.wind_kph} kph, "
                f"Condition: {self.condition_text}, Condition Code: {self.condition_code}, "
                f"Localtime: {self.localtime.strftime('%Y-%m-%d %H:%M:%S')}>")
