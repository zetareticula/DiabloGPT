import os
import sys
import importlib
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# List of modules to test
MODULES_TO_TEST = [
    "AML.Synthetic.EINSTEINAI4DB.deep_rl.join_data_preparation",
    "AML.Synthetic.EINSTEINAI4DB.ensemble_creation.utils",
    "ensemble_compilation.graph_representation",
    "DiabloGPT.Database",
    "DiabloGPT.GCN"
]

def test_module_import(module_name):
    """Test if a module can be imported and list its contents."""
    print(f"\n{'='*80}")
    print(f"Testing import of: {module_name}")
    print("-" * 80)
    
    try:
        module = importlib.import_module(module_name)
        print(f"✅ Successfully imported: {module_name}")
        
        # List top-level functions/classes in the module
        print("\nTop-level items in module:")
        for item in dir(module):
            if not item.startswith('_'):
                print(f"- {item}")
                
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        print("\nPython path:")
        for path in sys.path:
            print(f"- {path}")
    except Exception as e:
        print(f"⚠️ Error while processing {module_name}: {e}")

if __name__ == "__main__":
    print("Testing DiabloGPT project structure...")
    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version}")
    
    # Test each module
    for module_name in MODULES_TO_TEST:
        test_module_import(module_name)
    
    print("\nTest completed!")
