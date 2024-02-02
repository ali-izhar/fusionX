import os
import secrets

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', default=secrets.token_hex(16))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024       # 16MB
    