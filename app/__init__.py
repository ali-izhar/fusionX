from flask import Flask, render_template
from config.config import Config
from dotenv import load_dotenv
import logging

load_dotenv()

# enable logging
logging.disable(logging.NOTSET)

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    from .views import main_bp
    app.register_blueprint(main_bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app