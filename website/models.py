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

from website import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"
