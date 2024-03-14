import os
import torch
from torch.optim import LBFGS
import torch.nn.functional as F
from torch.nn.utils import clip_grad_value_

from vgg19 import Vgg19
from utils import prepare_img, save_and_maybe_display, total_variation, gram_matrix, setup_paths


def prepare_model(device):
    """Load VGG19 model into local cache, optimized for the given device."""
    model = Vgg19(requires_grad=False, show_progress=True).to(device).eval()
    content_feature_maps_index = model.content_feature_maps_index
    layer_names = model.layer_names

    content_fms_index = content_feature_maps_index
    style_fms_indices = [i for i in range(len(layer_names)) if i != content_feature_maps_index]
    return model, content_fms_index, style_fms_indices


def build_loss(neural_net, optimizing_img, target_representations, 
               content_feature_maps_index, style_feature_maps_indices, config):
    """Calculate content_loss, style_loss, and total_variation_loss."""
    target_content, target_style = target_representations
    current_features = neural_net(optimizing_img)
    current_content = current_features[content_feature_maps_index].squeeze(0)
    
    # Content loss, scale down if necessary
    content_loss = F.mse_loss(current_content, target_content)
    content_loss = content_loss / (current_content.size(0) * current_content.size(1) * current_content.size(2))

    # Style loss, scale down if necessary
    style_losses = []
    for i, style_index in enumerate(style_feature_maps_indices):
        gram_current = gram_matrix(current_features[style_index].squeeze(0))
        gram_target = target_style[i]
        style_losses.append(F.mse_loss(gram_current, gram_target, reduction='sum') / gram_current.numel())
    style_loss = sum(style_losses) / (len(style_losses) + 1e-6)

    # Make sure style_loss is not NaN
    if torch.isnan(style_loss).any():
        raise ValueError('NaN values encountered in the style loss')

    # Total variation loss
    tv_loss = total_variation(optimizing_img)

    # Apply the weights from the config
    content_loss *= config['content_weight']
    style_loss *= config['style_weight']
    tv_loss *= config['tv_weight']

    # Compute total loss
    total_loss = content_loss + style_loss + tv_loss
    return total_loss, content_loss, style_loss, tv_loss


def make_tuning_step(neural_net, optimizer, target_representations, 
                     content_feature_maps_index, style_feature_maps_indices, config):
    """Create a function to perform a tuning step in the optimization loop."""
    def tuning_step(optimizing_img):
        # Calculate losses
        total_loss, content_loss, style_loss, tv_loss = build_loss(
            neural_net, optimizing_img, target_representations,
            content_feature_maps_index, style_feature_maps_indices, config)

        # Perform optimization step
        optimizer.zero_grad()  # Clear gradients before backward pass
        total_loss.backward()  # Backpropagate
        optimizer.step()       # Update optimizing image

        return total_loss, content_loss, style_loss, tv_loss

    return tuning_step


def neural_style_transfer(config):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    content_img, style_img = [prepare_img(config[path_key], config['height'], device) 
                              for path_key in ['content_img_path', 'style_img_path']]
    
    optimizing_img = content_img.clone().requires_grad_(True)
    neural_net, content_fms_index, style_fms_indices = prepare_model(device)
    
    print('Using VGG19 in the optimization procedure.')

    target_content_representation, target_style_representation = None, None
    with torch.no_grad():
        target_content_representation = neural_net(content_img)[content_fms_index].squeeze(0)
        target_style_representation = [gram_matrix(neural_net(style_img)[i].squeeze(0)) 
                                       for i in style_fms_indices]

    # LBFGS optimizer: the optimizer will perform 100 optimization steps, but the closure function
    # per iteration might be called multiple times, depending on the line search algorithm.
    # Therefore, the number of iterations might be slightly higher than 100.
    optimizer = LBFGS([optimizing_img], max_iter=config['num_iterations'], line_search_fn='strong_wolfe')

    cnt = 0
    while cnt <= config['num_iterations']:
        def closure():
            nonlocal cnt
            optimizer.zero_grad()
            total_loss, content_loss, style_loss, tv_loss = build_loss(
                neural_net, optimizing_img, 
                [target_content_representation, target_style_representation], 
                content_fms_index, style_fms_indices, config)
            
            if total_loss.requires_grad:
                total_loss.backward()
            
            clip_grad_value_(optimizing_img, 1)

            # Check for NaN values
            if torch.isnan(total_loss).any():
                raise ValueError(f'NaN values encountered in the total loss at iteration {cnt}')

            with torch.no_grad():
                print(f'iter [{cnt:03}]\ttotal loss={total_loss.item():6.4f}\tcontent_loss={config["content_weight"] * content_loss.item():6.4f}\tstyle loss={config["style_weight"] * style_loss.item():6.4f}\ttv loss={config["tv_weight"] * tv_loss.item():6.4f}')
                save_and_maybe_display(optimizing_img, cnt, config)
            
            cnt += 1
            return total_loss

        optimizer.step(closure)

        # Check for NaN values
        if torch.isnan(optimizing_img).any():
            raise ValueError(f'NaN values encountered in the optimizing image at iteration {cnt}')

    return os.path.join(config['output_img_dir'], config['output_img_name'])


def main():
    config = {
        'content_images_dir': './data/content-images',
        'style_images_dir': './data/style-images',
        'content_img_name': 'content.jpg',
        'style_img_name': 'style.png',
        'output_img_dir': './data/output-images',
        'output_img_name': 'output.jpg',
        'height': 500,
        'content_weight': 1.0,
        'style_weight': 30,
        'tv_weight': 1e-1,
        'num_iterations': 100,
    }
    config['img_format'] = (4, '.jpg')
    setup_paths(config)
    
    results_path = neural_style_transfer(config)
    print(f"Neural style transfer completed. Results saved to {results_path}")

if __name__ == "__main__":
    main()
