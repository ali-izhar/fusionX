import os
import random
import base64
import traceback
import logging

# define gallery blueprint
gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@gallery_bp.route('/')
def gallery():
    # get all gallery images
    images = [f for f in os.listdir('app/static/img') if f.endswith('.png')]
    return render_template('gallery.html', images=images)


@gallery_bp.route('/gallery_image/<path:img_name>', methods=['GET'])
def gallery_image(img_name):
    try:
        file_path = f"app/static/img/{img_name}"
        with open(file_path, "rb") as img_file:
            image = base64.b64encode(img_file.read()).decode('utf-8')
        image_data = f"data:image/png;base64,{image}"
        return render_template("result.html", image=image_data, prompt="Gallery Image", user=current_user)
    except Exception as e:
        logging.error(f"[Function: gallery_image] Error serving image: {e}")
        return render_template("error.html")