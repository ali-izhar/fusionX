import os
import secrets

class Config:
    """Set Flask configuration variables.
    - SECRET_KEY: A secret key for a particular Flask session.
    - ALLOWED_EXTENSIONS: A set of allowed file extensions for file uploads.
    - MAX_CONTENT_LENGTH: The maximum file size for file uploads (16MB)
    - UPLOAD_FOLDER: The folder where uploaded files are stored.
    - OUTPUT_FOLDER: The folder where generated images are stored.
    - MODEL_PATH: The path to the RealESRGAN model file.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', default=secrets.token_hex(16))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    OUTPUT_FOLDER = 'outputs'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # RealESRGAN model path
    MODEL_PATH = 'editor/models/RealESRGAN_x4plus.pth'
    os.makedirs('editor/models', exist_ok=True)