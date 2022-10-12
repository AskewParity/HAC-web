from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from HAC_app.config import Config
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'grades.login_page'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask("Flask App", template_folder='./HAC_app/templates', static_folder='./HAC_app/static')
    #test
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.config.from_object(Config)

    from HAC_app.main.views import main
    from HAC_app.grades.views import user
    from HAC_app.errors.handlers import errors

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(user)

    return app
