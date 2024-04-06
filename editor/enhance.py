import base64
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from utils.nst_utils import base64_to_PIL
from config import Config

def download_model(model_path, url):
    """Downloads the model if not found."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print('Model downloaded successfully.')
    except requests.RequestException as e:
        print(f"Failed to download the model: {e}")

def initialize_upsampler():
    """Initializes the upsampler model, downloading it if necessary."""
    model_path = Config.MODEL_PATH
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    try:
        upsampler = RealESRGANer(scale=2, model_path=model_path, model=model, tile=0, tile_pad=10, pre_pad=0, half=False)
    except FileNotFoundError:
        print("RealESRGAN weights not found, downloading...")
        download_model(model_path, 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth')
        upsampler = RealESRGANer(scale=4, model_path=model_path, model=model, tile=0, tile_pad=10, pre_pad=0, half=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    return upsampler


def enhance_image(b64_string, upsampler, max_width=1024, max_height=1024):
    """Enhances the image encoded in a base64 string using the given upsampler.
    Returns a tuple of (result_image_base64, was_enhanced)"""
    image = base64_to_PIL(b64_string)

    # Check image dimensions to avoid re-enhancing large images
    if image.width > max_width or image.height > max_height:
        print("Image is already large, skipping enhancement.")
        output = np.array(image)
        was_enhanced = False  # Indicate that the image was not enhanced
    else:
        image_np = np.array(image)
        output, _ = upsampler.enhance(image_np, outscale=4)
        was_enhanced = True  # Image was enhanced

    result_image = Image.fromarray(output)
    buffer = BytesIO()
    result_image.save(buffer, format="PNG")
    result_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return result_image_base64, was_enhanced
