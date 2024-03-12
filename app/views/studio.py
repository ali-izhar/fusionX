import base64
import os
import requests
from io import BytesIO
from flask import Blueprint, request, render_template, session, redirect, url_for
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

    # Fetch the image from the URL
    response = requests.get(result_image_url)
    result_image_data = BytesIO(response.content)

    # Convert the resulting image data to base64 to send back
    result_image_base64 = base64.b64encode(result_image_data.getvalue()).decode('utf-8')

    # Store the base64 image in session to display on the result page
    session['result_image_base64'] = result_image_base64
    return redirect(url_for('studio_bp.show_result'))


@studio_bp.route('/result')
def show_result():
    image_path = session.get('result_image_path', '')
    return render_template('result.html', image_path=image_path)


def save_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_path = f"static/images/{os.path.basename(url)}"
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    return None


def dalle(prompt, model="dall-e-3", quality="standard", n=1):
    """Generate images using OpenAI's DALL-E model with the given prompt."""
    response = client.images.generate(
            model=model,
            prompt=prompt,
            quality=quality,
            n=n,
        )
    return response.data[0].url
