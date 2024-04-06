#!/bin/bash

# Install common dependencies
pip install -r requirements.txt

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
