import base64
import logging
import os
import tempfile
from flask import jsonify, request, Blueprint, render_template
from nst import neural_style_transfer
from openai import OpenAI
from config import Config

from utils.nst_utils import (process_image_data, write_temp_file, cleanup_temp_files,
                    generate_unique_file_name, generate_image_with_dalle)

client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY')
studio_bp = Blueprint('studio_bp', __name__, url_prefix='/studio')


@studio_bp.route('/result')
def result():
    return render_template('result.html')


@studio_bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    image_data = generate_image_with_dalle(client, prompt)
    return render_template('result.html', image_data=image_data)


@studio_bp.route('/merge', methods=['POST'])
def merge():
    data = request.get_json()
    content_data = data['contentImage']  # base64 encoded string or URL
    style_data = data['styleImage']  # base64 encoded string or URL

    try:
        # Process content and style images
        content_image_data, content_extension = process_image_data(content_data)
        style_image_data, style_extension = process_image_data(style_data)

        # Create temporary files for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{content_extension}') as content_temp_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=f'.{style_extension}') as style_temp_file:

            write_temp_file(content_temp_file, content_image_data)
            write_temp_file(style_temp_file, style_image_data)

            # Perform neural style transfer and generate result
            result_image_base64 = perform_neural_style_transfer(content_temp_file.name, style_temp_file.name, data)

            # Close temporary files before cleanup
            content_temp_file.close()
            style_temp_file.close()
            
            # Cleanup and return result
            cleanup_temp_files([content_temp_file.name, style_temp_file.name])
            return jsonify({'result': f"data:image/jpeg;base64,{result_image_base64}"})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to process images'}), 500


def perform_neural_style_transfer(content_path, style_path, settings):
    """Performs neural style transfer with the given settings and returns
    the result as a base64 encoded string.
    """
    original_file_name = settings.get('settings', {}).get('outputFileName', 'output')
    img_format = settings.get('settings', {}).get('outputImageFormat', '.jpg')

    # Generate a unique file name if necessary
    output_file_name = generate_unique_file_name(Config.OUTPUT_FOLDER, original_file_name, img_format)

    config = {
        'content_img_path': content_path,
        'style_img_path': style_path,
        'output_file_name': output_file_name,
        'img_format': img_format,
        'height': int(settings.get('settings', {}).get('nstImageHeight', 512)),
        'content_weight': float(settings.get('settings', {}).get('nstContentWeight', 1.0)),
        'style_weight': float(settings.get('settings', {}).get('nstStyleWeight', 30)),
        'tv_weight': float(settings.get('settings', {}).get('nstTotalVariationWeight', 1e-1)),
        'num_iterations': int(settings.get('settings', {}).get('nstIterations', 10)),
    }
    config['output_img_path'] = os.path.join(Config.OUTPUT_FOLDER, config['output_file_name'])

    # Perform neural style transfer using the provided configuration
    neural_style_transfer(config)

    # Read the result and encode it into base64
    with open(config['output_img_path'], "rb") as result_image_file:
        return base64.b64encode(result_image_file.read()).decode('utf-8')