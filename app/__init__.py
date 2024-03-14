from config.config import Config
from dotenv import load_dotenv
from flask import Flask, render_template
import logging

load_dotenv()

# enable logging
logging.disable(logging.NOTSET)


def create_app(config_class=Config):
    logging.info('Creating app...')
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    logging.info('Registering blueprints...')
    from .views import main_bp, studio_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(studio_bp)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app