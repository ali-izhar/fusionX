import requests
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionUpscalePipeline
import torch

def upscale(image, prompt):
    model_id = "stabilityai/stable-diffusion-x4-upscaler"
    pipeline = StableDiffusionUpscalePipeline.from_pretrained(
        model_id, revision="fp16", torch_dtype=torch.float16
    )
    pipeline = pipeline.to("cuda")

    # let's download an  image
    low_res_img = image
    prompt = prompt

    upscaled_image = pipeline(prompt=prompt, image=low_res_img).images[0]
    return upscaled_image


if __name__ == "__main__":
    img = Image.open("./output.jpg")
    prompt = "a style transfer using NST"
    upscaled_image = upscale(img, prompt)
    upscaled_image.show()