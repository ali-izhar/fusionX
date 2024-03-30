from collections import namedtuple
import torch
from torchvision.models import vgg19, VGG19_Weights

class Vgg19(torch.nn.Module):
    """VGG-19 has a total of 19 layers.
        - conv4_2 is used for content representation.
        - conv1_1, conv2_1, conv3_1, conv4_1, and conv5_1 are used for style representation.
    """
    def __init__(self, requires_grad=False, show_progress=False):
        super().__init__()
        vgg_pretrained_features = vgg19(weights=VGG19_Weights.DEFAULT, progress=show_progress).features

        self.layer_names = ['relu1_1', 'relu2_1', 'relu3_1', 'relu4_1', 'conv4_2', 'relu5_1']
        self.offset = 1
        self.content_feature_maps_index = 4
        self.style_feature_maps_indices = list(range(len(self.layer_names)))
        self.style_feature_maps_indices.remove(4)
        
        # Initialize ModuleList to store the slices
        self.slices = torch.nn.ModuleList()
        
        # Define the end index for each slice to streamline loop definitions
        slice_end_indices = [1+self.offset, 6+self.offset, 11+self.offset, 20+self.offset, 22, 29+self.offset]
        
        start_idx = 0
        for end_idx in slice_end_indices:
            # Create a Sequential module for each slice and add it to ModuleList
            slice_ = torch.nn.Sequential()
            for x in range(start_idx, end_idx):
                slice_.add_module(str(x), vgg_pretrained_features[x])
            self.slices.append(slice_)
            start_idx = end_idx
            
        if not requires_grad:
            for param in self.parameters():
                param.requires_grad = False

    def forward(self, x):
        results = []
        for slice_ in self.slices:
            x = slice_(x)
            results.append(x)
        
        # Use the results directly to construct the namedtuple
        vgg_outputs = namedtuple("VggOutputs", self.layer_names)
        out = vgg_outputs(*results)
        
        return out