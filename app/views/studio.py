from flask import Blueprint, request, render_template, redirect, url_for, jsonify
import base64
from io import BytesIO
from PIL import Image

studio_bp = Blueprint('studio_bp', __name__, url_prefix='/studio')

@studio_bp.route('/merge', methods=['POST'])
def merge():
    data = request.get_json()
    content_data = data['contentImage']  # base64 encoded string
    style_data = data['styleImage']  # base64 encoded string

    # Decode the base64 strings
    content_image_data = base64.b64decode(content_data.split(',')[1])
    style_image_data = base64.b64decode(style_data.split(',')[1])

    # Convert to PIL Image
    content_image = Image.open(BytesIO(content_image_data))
    style_image = Image.open(BytesIO(style_image_data))

    # TODO: Perform the merge operation with the images here
    # Let's say the result is stored in a PIL image called result_image
    result_image = content_image

    # Convert the resulting PIL Image to base64 to send back
    buffered = BytesIO()
    result_image.save(buffered, format="PNG")
    result_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({
        'contentImage': content_data,
        'styleImage': style_data,
        'resultImage': f"data:image/png;base64,{result_image_base64}"
    })


def merge_images(content, style):
    # Your image merging logic goes here
    # For now, let's just return the content image
    return content