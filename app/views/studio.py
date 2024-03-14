import base64
import os
import requests
from io import BytesIO
from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
# from app import app

from openai import OpenAI
# from ...NST import neural_style_transfer

client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY')
studio_bp = Blueprint('studio_bp', __name__, url_prefix='/studio')


@studio_bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    image_data = dalle(prompt)
    return render_template('result.html', image_data=image_data)


# @studio_bp.route('/merge', methods=['POST'])
# def merge():
    # # Check if the post request has the file part
    # if 'contentUpload' not in request.files or 'styleUpload' not in request.files:
    #     return jsonify({'error': 'No file part'}), 400

    # content_file = request.files['contentUpload']
    # style_file = request.files['styleUpload']

    # # If the user does not select a file, the browser submits an empty part without a filename
    # if content_file.filename == '' or style_file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400

    # if content_file and style_file:
    #     content_filename = secure_filename(content_file.filename)
    #     style_filename = secure_filename(style_file.filename)
    #     content_path = os.path.join(app.config['UPLOAD_FOLDER'], content_filename)
    #     style_path = os.path.join(app.config['UPLOAD_FOLDER'], style_filename)
        
    #     content_file.save(content_path)
    #     style_file.save(style_path)

    #     # Perform Neural Style Transfer
    #     # result_image_path = perform_nst(content_path, style_path)  # Adapt arguments as needed
        
    #     # Read and encode the resulting image to base64
    #     with open(result_image_path, "rb") as image_file:
    #         result_image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    #     # Return a JSON response with the base64 encoded image
    #     return jsonify({'result': f"data:image/png;base64,{result_image_base64}"})


@studio_bp.route('/merge', methods=['POST'])
def merge():
    data = request.get_json()
    random_prompt = "a sports car with a sunset in the background"
    result_image_url = dalle(random_prompt)

    # Fetch the image from the URL provided by DALL-E
    response = requests.get(result_image_url)
    if response.status_code == 200:
        # Convert the resulting image data to base64 to send back
        result_image_base64 = base64.b64encode(BytesIO(response.content).getvalue()).decode('utf-8')

        # Return a JSON response with the base64 encoded image
        return jsonify({'result': f"data:image/png;base64,{result_image_base64}"})
    else:
        return jsonify({'error': 'Failed to retrieve image from DALL-E'}), 500


@studio_bp.route('/result')
def result():
    return render_template('result.html')


def dalle(prompt, model="dall-e-3", quality="standard", n=1):
    """Generate images using OpenAI's DALL-E model with the given prompt."""
    response = client.images.generate(
            model=model,
            prompt=prompt,
            quality=quality,
            n=n,
        )
    return response.data[0].url
