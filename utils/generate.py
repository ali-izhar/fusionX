import io
import os
import base64
from PIL import Image
import requests
import logging

__all__ = ["Model", "ModelError", "generate_image_with_dalle"]

headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
TIMEOUT = 60

class ModelError(Exception):
    pass

class Model:
    def __init__(self, selected_model, prompt, negative_prompt, guidance_scale, inference_steps, height, width):
        self.selected_model = selected_model
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.params = {
            "inputs": self.prompt,
            "parameters": {
                "negative_prompt": self.negative_prompt,
                "guidance_scale": guidance_scale,
                "num_inference_steps": inference_steps,
                "height": height,
                "width": width
            },
            "options": {
                "seed": 42,
                "temperature": 0.5,
                "use_cache": False,
                "wait_for_model": True
            }
        }

    def generate(self):
        try:
            base_64_image = self._generate_image()
            return base_64_image
        except Exception as e:
            logging.error(f"Failed to generate image: {e}")
            raise ModelError(f"Failed to generate image: {e}") from e

    def _generate_image(self):
        response_content = self.fetch_response()
        if not response_content:
            raise ModelError("No content in the response")

        image = Image.open(io.BytesIO(response_content))
        image_byte_data = io.BytesIO()
        image.save(image_byte_data, format='PNG')
        base_64_image = base64.b64encode(image_byte_data.getvalue()).decode('utf-8')
        return base_64_image

    def fetch_response(self):
        try:
            response = requests.post(
                self.selected_model,
                headers=headers,
                json=self.params,
                timeout=TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"RequestException: {e}")
            raise ModelError(f"RequestException: {e}") from e

        if response.status_code != 200:
            error_msg = f"Failed to generate image: {response.status_code}"
            logging.error(error_msg)
            logging.error(f"Response text: {response.text}")
            raise ModelError(error_msg)

        return response.content


def generate_image_with_dalle(client, prompt, model="dall-e-3", quality="standard", n=1):
    """Generate images using OpenAI's DALL-E model with the given prompt."""
    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            quality=quality,
            n=n,
        )
        return response.data[0].url
    except Exception as e:
        logging.error(f"An error occurred while generating image with DALL-E: {e}")
        raise e