import os
import logging
import cv2 as cv
import numpy as np
import torch
from torchvision import transforms

IMAGENET_MEAN_255 = [123.675, 116.28, 103.53]
IMAGENET_STD_NEUTRAL = [1, 1, 1]


def gram_matrix(x):
    """Generate gram matrices of the representations of content and style images."""
    if x.dim() == 3:
        x = x.unsqueeze(0)  # Add a batch dimension if missing
    
    b, ch, h, w = x.size()
    features = x.view(b, ch, w * h)
    G = features.bmm(features.transpose(1, 2))
    return G.div(ch * h * w * b)    # additional normalization by batch size


def total_variation(y):
    """Calculate total variation to encourage spatial smoothness."""
    batch_size, channels, height, width = y.size()
    tv_height = torch.abs(y[:, :, :-1, :] - y[:, :, 1:, :]).sum()
    tv_width = torch.abs(y[:, :, :, :-1] - y[:, :, :, 1:]).sum()
    return (tv_height + tv_width) / (batch_size * channels * height * width)


def load_image(img_path, target_shape=None):
    """Load an image from a file and convert it to a numpy array."""
    if not os.path.exists(img_path):
        logging.error(f'Function: [load_image] - Path not found: {img_path}')
        raise FileNotFoundError(f'Path not found: {img_path}')
    
    img = cv.imread(img_path, cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if target_shape is not None:
        if isinstance(target_shape, int) and target_shape > 0:
            ratio = target_shape / img.shape[1]
            new_shape = (target_shape, int(img.shape[0] * ratio))
        elif isinstance(target_shape, tuple):
            new_shape = (target_shape[1], target_shape[0])
        else:
            logging.error(f'Function: [load_image] - Invalid target_shape value')
            raise ValueError("Invalid target_shape value")
        img = cv.resize(img, new_shape, interpolation=cv.INTER_CUBIC)
    
    img = img.astype(np.float32) / 255.0
    return img


def prepare_img(img_path, target_shape, device):
    """Normalize the image."""
    if not os.path.exists(img_path):
        logging.error(f'Function: [prepare_img] - Path not found: {img_path}')
        raise FileNotFoundError(f'Path not found: {img_path}')
    
    img = load_image(img_path, target_shape)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255)),
        transforms.Normalize(mean=IMAGENET_MEAN_255, std=IMAGENET_STD_NEUTRAL)])
    img = transform(img).to(device).unsqueeze(0)
    return img


def save_image(img, img_path):
    """Save an image to a file."""
    if not isinstance(img, np.ndarray):
        logging.error(f'Function: [save_image] - img should be a numpy array')
        raise ValueError('img should be a numpy array')
    
    if len(img.shape) == 2:
        img = np.stack((img,) * 3, axis=-1)

    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    cv.imwrite(img_path, img)


def save_and_maybe_display(optimizing_img, img_id, iters, img_path):
    """Save the generated image.
    If saving_freq == -1, only the final output image will be saved.
    Else, intermediate images can be saved too.
    """
    saving_freq = -1
    out_img = optimizing_img.squeeze(axis=0).to('cpu').detach().numpy()
    out_img = np.moveaxis(out_img, 0, 2)

    if img_id == iters - 1 or saving_freq == -1 or (img_id % saving_freq == 0):
        dump_img = np.copy(out_img)
        dump_img += np.array(IMAGENET_MEAN_255).reshape((1, 1, 3))
        dump_img = np.clip(dump_img, 0, 255).astype('uint8')
        save_image(dump_img, img_path)
