import os
from flask import Blueprint, render_template
from utils.data import MODELS

main_bp = Blueprint('main_bp', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    carousel_images = os.listdir('app/static/img/carousel')
    return render_template('index.html', carousel_images=carousel_images)

@main_bp.route('/studio')
def studio():
    return render_template('studio.html', models=MODELS)

@main_bp.route('/gallery')
def gallery():
    images = os.listdir('app/static/img/gallery')
    return render_template('gallery.html', images=images)

@main_bp.route('/docs')
def docs():
    return render_template('docs.html')