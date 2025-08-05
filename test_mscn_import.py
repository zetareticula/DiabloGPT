#!/usr/bin/env python3
"""
Test script to verify that the mscn module can be imported.
"""
import sys
import os

# Add the parent directory of the mscn module to the Python path
learnedcardinalities_path = os.path.abspath(os.path.join('AML', 'Transformers', 'learnedcardinalities-master'))
sys.path.insert(0, learnedcardinalities_path)

try:
    print("Attempting to import mscn module...")
    import mscn
    from mscn import data, model, preprocessing, util
    
    print("Successfully imported mscn module!")
    print(f"mscn module path: {mscn.__file__}")
    
    # Test if we can create a model
    print("\nTesting model creation...")
    sample_feats = 5
    predicate_feats = 20
    join_feats = 10
    hid_units = 256
    model = mscn.model.SetConv(sample_feats, predicate_feats, join_feats, hid_units)
    print(f"Successfully created model: {model}")
    
except ImportError as e:
    print(f"Error importing mscn module: {e}")
    import traceback
    traceback.print_exc()
    raise
