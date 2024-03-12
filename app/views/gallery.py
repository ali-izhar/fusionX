from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery_bp', __name__, url_prefix='/gallery')

@gallery_bp.route('/')
def index():
    return render_template('gallery/index.html')