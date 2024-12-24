import os
from dotenv import load_dotenv

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'WeatherDB')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable the warning about track modifications
    SECRET_KEY = os.urandom(24)  # Used for securing sessions, cookies, etc.
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    # Example: 'postgresql://postgres:password@localhost/myflaskdb'
 