#!/usr/bin/env python3
"""
Test script to verify that the main modules can be imported.
"""

try:
    import torch
    import numpy as np
    import scipy
    import tqdm
    import loguru
    import matplotlib
    import autoray
    
    # Try importing project-specific modules
    try:
        from DiabloGPT import Database
        print("Successfully imported DiabloGPT.Database")
    except ImportError as e:
        print(f"Could not import DiabloGPT.Database: {e}")
    
    print("\nAll required packages are installed and can be imported!")
    print(f"PyTorch version: {torch.__version__}")
    print(f"NumPy version: {np.__version__}")
    print(f"SciPy version: {scipy.__version__}")
    
except ImportError as e:
    print(f"Error: {e}")
    print("\nSome required packages are missing. Please install them using:")
    print("pip install torch numpy scipy tqdm loguru matplotlib autoray")
