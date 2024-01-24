from flask import Blueprint, render_template, session
from flask_login import current_user, login_user
from app.data import PLANS, MODELS
from app.services import get_user_by_email
from .auth import google_auth

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    session.permanent = False
    if 'oauth_token' in session:
        info = google_auth.authorized_response()
        email = info['email']
        user = get_user_by_email(email)
        if user:
            login_user(user)
    return render_template("index.html", user=current_user,  models=MODELS)

@main_bp.route('/status')
def status():
    return 'OK', 200