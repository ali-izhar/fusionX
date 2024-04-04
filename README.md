![GitHub contributors](https://img.shields.io/github/contributors/ali-izhar/fusionX)

# Fusion Xperience :fire: :zap:

**FusionX** is a Flask-based web application that brings the power of neural style transfer to your fingertips. Transform ordinary images into extraordinary pieces of art by applying the styles of famous paintings.

![fusionX App](./screenshots/index.jpg)

## :sparkles: Repository Vision

The goal of this repository is to provide a simple and easy-to-use web application for neural style transfer. The application is built using the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework and the [PyTorch](https://pytorch.org/) library. The neural style transfer model is based on the [A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576) paper by Leon A. Gatys, Alexander S. Ecker, and Matthias Bethge.

## :bookmark_tabs: Table of Contents

- [Features](#features-sparkles)
- [Application Preview](#application-preview-camera)
- [Getting Started](#getting-started-rocket)
  - [Prerequisites](#prerequisites-clipboard)
  - [Installation](#installation-computer)
- [Contributing](#contributing-handshake)
- [License](#license-page_facing_up)

## Features :sparkles:

- Upload or Generate content images
  - Upload from your device
  - Generate using Hugging Face Text-to-Image API
- Apply styles to content images
  - Upload from your device
  - Choose from a gallery of pre-loaded styles
  - Generate using Hugging Face Text-to-Image API
- Customize the style transfer process with advanced options
  - Adjust the style weight
  - Adjust the content weight
  - Adjust the total variation weight
  - Adjust the number of iterations
- Use the Editor to fine-tune the stylized image
  - Crop and Resize the image
  - Super Resolution using Real-ESRGAN
- Download the stylized image

<table>
<tr>
    <td>
        The Studio page allows you to upload content and style images.<br>
        <img src="./screenshots/studio.jpg" alt="Upload Image" width="100%"/>
    </td>
    <td>
        The Studio page also allows you to generate content and style images using the Hugging Face Text-to-Image API.<br>
        <img src="./screenshots/studio_modal.jpg" alt="Generate Image" width="100%"/>
    </td>
</tr>
<tr>
    <td>
        The Gallery page showcases a collection of pre-loaded style images that can be applied to your content images.<br>
        <img src="./screenshots/gallery.jpg" alt="Gallery" width="100%"/>
    </td>
    <td>
        Once both the content and style images are selected, you can customize the style transfer process using advanced options.<br>
        <img src="./screenshots/studio_merge.jpg" alt="Advanced Options" width="100%"/>
    </td>
</tr>
<tr>
    <td colspan="2">
        The Editor page allows you to fine-tune the stylized image by cropping, resizing, and enhancing the image.<br>
        <img src="./screenshots/editor.jpg" alt="Editor" width="100%"/>
    </td>
</tr>
</table>


## Getting Started :rocket:

#### Prerequisites :clipboard:

- Python 3.9 or higher
- Torch

#### Installation :computer:
```
# 1. Clone the repository
git clone https://github.com/yourusername/fusionX.git

# 2. Navigate to the project directory
cd fusionX

# 3. Create a virtual environment (optional)
python -m venv venv

# 4. Activate the virtual environment
source venv/bin/activate

# 5. Install the required packages
pip install -r requirements.txt

# 6. Run the application
python run.py
```

## Contributing :handshake:

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please refer to the [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License :page_facing_up:

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
