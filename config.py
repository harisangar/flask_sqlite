import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable the warning about track modifications
    SECRET_KEY = os.urandom(24)  # Used for securing sessions, cookies, etc.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/WeatherDB'
    # Example: 'postgresql://postgres:password@localhost/myflaskdb'
