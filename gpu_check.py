"""
    # gpu_check.py
    Check if the machine has available GPU
"""

import torch

def gpu_check():
    if torch.cuda.is_available():
        print("CUDA (GPU) is available. Version: ", torch.version.cuda)
        return True
    else:
        print("CUDA (GPU) is not available. Using CPU.")
        return False
