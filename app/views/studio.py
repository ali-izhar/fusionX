import base64
import os
import requests
from io import BytesIO
from flask import Blueprint, request, render_template, jsonify
from openai import OpenAI

client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY')
studio_bp = Blueprint('studio_bp', __name__, url_prefix='/studio')


@studio_bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    image_data = dalle(prompt)
    return render_template('result.html', image_data=image_data)


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
