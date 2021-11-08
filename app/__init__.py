from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_moment import Moment 



login = LoginManager()
#where to be sent if you are not logged in
login.login_view = 'auth.login'
login.login_message = "You must be logged in to view the page"
login.login_message_category = "warning"
# init the database from_object
db = SQLAlchemy()
migrate = Migrate()
# moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #register plugins
    login.init_app(app)    
    db.init_app(app)
    migrate.init_app(app,db)
    # moment.init_app(app)
    
    # Register our blueprints with the app
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.social import bp as social_bp
    app.register_blueprint(social_bp)

    return app