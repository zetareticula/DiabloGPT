import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try importing the main module
try:
    import maqp
    print("Successfully imported maqp module!")
    
    # Try to list available functions in the module
    print("\nAvailable functions in maqp module:")
    for item in dir(maqp):
        if not item.startswith('_'):
            print(f"- {item}")
    
except ImportError as e:
    print(f"Error importing maqp module: {e}")
    print("\nTrying to import submodules directly...")
    
    try:
        from AML.Synthetic.EINSTEINAI4DB.deep_rl.join_data_preparation import prepare_sample_hdf
        print("Successfully imported prepare_sample_hdf from AML.Synthetic.EINSTEINAI4DB.deep_rl.join_data_preparation")
    except ImportError as e:
        print(f"Error importing submodule: {e}")
        print("\nPython path:")
        for path in sys.path:
            print(f"- {path}")
