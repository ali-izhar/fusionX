import base64
import logging
import os
import requests
import time
import tempfile
from flask import jsonify, request, Blueprint, render_template
from NST import neural_style_transfer
from openai import OpenAI
from config import Config

client = OpenAI()

client.api_key = os.environ.get('OPENAI_API_KEY')
studio_bp = Blueprint('studio_bp', __name__, url_prefix='/studio')


@studio_bp.route('/result')
def result():
    return render_template('result.html')


@studio_bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    image_data = dalle(prompt)
    return render_template('result.html', image_data=image_data)


@studio_bp.route('/merge', methods=['POST'])
def merge():
    data = request.get_json()
    content_data = data['contentImage']  # base64 encoded string or URL
    style_data = data['styleImage']  # base64 encoded string or URL

    try:
        # Check and process content image data
        if not is_base64(content_data):
            logging.info("Content data is not base64. Attempting to convert from URL.")
            content_data = convert_to_base64(content_data)
            if content_data is None:
                logging.error("Failed to convert content image data to base64.")
                return jsonify({'error': 'Failed to convert content image data to base64.'}), 400
        # Decode base64 (now we're sure it is base64)
        content_image_data = base64.b64decode(content_data.split(',')[1])

        # Check and process style image data
        if not is_base64(style_data):
            logging.info("Style data is not base64. Attempting to convert from URL.")
            style_data = convert_to_base64(style_data)
            if style_data is None:
                logging.error("Failed to convert style image data to base64.")
                return jsonify({'error': 'Failed to convert style image data to base64.'}), 400
        # Decode base64 (now we're sure it is base64)
        style_image_data = base64.b64decode(style_data.split(',')[1])

        # get the extension of the content and style images to dynamically set the temp files
        content_extension = content_data.split(',')[0].split('/')[1].split(';')[0]
        style_extension = style_data.split(',')[0].split('/')[1].split(';')[0]

        print(content_extension, style_extension)

        # Create temporary files to store the images for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{content_extension}') as content_temp_file, \
                tempfile.NamedTemporaryFile(delete=False, suffix=f'.{style_extension}') as style_temp_file:

            content_temp_file.write(content_image_data)
            content_temp_file.flush()
            style_temp_file.write(style_image_data)
            style_temp_file.flush()

            # Define the configuration for NST
            config = {
                'content_img_path': content_temp_file.name,
                'style_img_path': style_temp_file.name,
                'output_file_name': data.get('settings', {}).get('outputFileName', 'output.jpg'),
                'img_format': data.get('settings', {}).get('outputImageFormat', (4, '.jpg')),
                'height': int(data.get('settings', {}).get('nstImageHeight', 512)),
                'content_weight': float(data.get('settings', {}).get('nstContentWeight', 1.0)),
                'style_weight': float(data.get('settings', {}).get('nstStyleWeight', 30)),
                'tv_weight': float(data.get('settings', {}).get('nstTotalVariationWeight', 1e-1)),
                'num_iterations': int(data.get('settings', {}).get('nstIterations', 10)),
            }
            config['output_img_path'] = os.path.join(Config.OUTPUT_FOLDER, config['output_file_name'] + config['img_format'])

            # Perform neural style transfer using the config
            neural_style_transfer(config)

            wait_for_file(config['output_img_path'])
            # Read the result and encode it into base64
            with open(config['output_img_path'], "rb") as result_image_file:
                result_image_base64 = base64.b64encode(result_image_file.read()).decode('utf-8')

            # Clean up temporary files
            content_temp_file.close()
            style_temp_file.close()

            os.remove(content_temp_file.name)
            os.remove(style_temp_file.name)

            return jsonify({'result': f"data:image/jpeg;base64,{result_image_base64}"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process images'}), 500


def is_base64(data):
    try:
        if 'data:image' in data and ';base64,' in data:
            return True
    except Exception as e:
        logging.error(f"An error occurred while checking base64 encoding: {e}")
    return False


def convert_to_base64(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"data:image/jpeg;base64,{base64.b64encode(response.content).decode('utf-8')}"
    except Exception as e:
        logging.error(f"An error occurred while converting image URL to base64: {e}")
    return None


def wait_for_file(file_path, timeout=10):
    """Wait for a file to be released by another process."""
    start_time = time.time()
    while True:
        try:
            # Try to open the file in append mode and immediately close it
            with open(file_path, 'a'):
                return True
        except PermissionError:
            # If a permission error is raised, the file is likely still in use
            if time.time() - start_time >= timeout:
                # If the timeout has been reached, raise an error
                raise TimeoutError(f"Timeout reached while waiting for file {file_path}")
            time.sleep(0.5)  # Wait a bit before trying again


def dalle(prompt, model="dall-e-3", quality="standard", n=1):
    """Generate images using OpenAI's DALL-E model with the given prompt."""
    response = client.images.generate(
            model=model,
            prompt=prompt,
            quality=quality,
            n=n,
        )
    return response.data[0].url
