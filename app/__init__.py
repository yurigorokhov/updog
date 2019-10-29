from flask import Flask
from pony.orm import *
from pony.flask import Pony
from flask_login import LoginManager
from .models import db
from .config import DevelopmentConfig




def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)
    Pony(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    




    with app.app_context():

        from . import routes
        db.bind(**app.config['PONY'])
        db.generate_mapping(create_tables=True)

        @login_manager.user_loader
        def load_user(user_id):
            return db.User.get(id=user_id)
       

        return app