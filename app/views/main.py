from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/studio')
def studio():
    return render_template('studio.html')

@main_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

@main_bp.route('/docs')
def docs():
    return render_template('docs.html')