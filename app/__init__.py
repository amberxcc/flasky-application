from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_mail import Mail
from config import config, Config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
pagedown = PageDown()

login_manager.login_view = 'auth.login'
redis_client = Config.REDIS_CLIENT

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 调用所选配置的 init_app() 方法，以便执行更复杂的初始化过程，这里init_app() 方法为空
    config[config_name].init_app(app)
    
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app