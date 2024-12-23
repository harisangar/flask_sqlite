from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# db = SQLAlchemy()
# DB_NAME="database.db"


website = Blueprint('website', __name__, template_folder='templates', static_folder='static')


def create_app():
    app=Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY']='secretkey'
    # app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
   
   
    db.init_app(app)
    migrate.init_app(app, db)

   
    
    from .views import views
    # from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    # app.register_blueprint(auth,url_prefix='/')

    # from .models import Note,User

    
    # create_database(app)
    # login_manager=LoginManager()
    # login_manager.login_view= 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))




    app.register_blueprint(website, url_prefix='')
    return app

# def create_database(app):
#      with app.app_context():
#         if not path.exists('website/' + DB_NAME):
#             db.create_all()  # Create the tables
#             print('Database created...')
