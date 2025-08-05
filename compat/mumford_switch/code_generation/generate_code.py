"""Code generation for the mumford_switch compatibility layer."""
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from ...structure import Node, Sum, Product, IdentityNumericLeaf, Categorical

class TemplatePath:
    """Helper class for template paths."""
    pass

def generate_code(node: Node, output_dir: str, class_name: str = "GeneratedModel") -> str:
    """
    Generate Python code that represents the SPN.
    
    Args:
        node: Root node of the SPN
        output_dir: Directory to save the generated code
        class_name: Name of the generated class
        
    Returns:
        Path to the generated file
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{class_name.lower()}.py")
    
    code = [
        '"""Auto-generated SPN model."""',
        'import numpy as np',
        'from scipy import stats',
        '',
        f'class {class_name}:'
        '    """Auto-generated SPN model."""
        '    
    def __init__(self):',
        '        self.root = self._build_model()',
        '    
    def _build_model(self):',
    ]
    
    # Generate code to build the SPN
    node_id = 0
    node_map = {}
    
    def generate_node_code(n, parent_var):
        nonlocal node_id
        
        if id(n) in node_map:
            return node_map[id(n)]
            
        if isinstance(n, Sum):
            var_name = f"sum_{node_id}"
            node_id += 1
            
            # Generate children code first
            children_vars = []
            for child in n.children:
                child_var = generate_node_code(child, var_name)
                children_vars.append(child_var)
            
            # Generate sum node code
            weights = ", ".join(str(w) for w in n.weights)
            children = ", ".join(children_vars)
            code.append(f'        {var_name} = Sum(children=[{children}], weights=[{weights}])')
            
        elif isinstance(n, Product):
            var_name = f"prod_{node_id}"
            node_id += 1
            
            # Generate children code first
            children_vars = []
            for child in n.children:
                child_var = generate_node_code(child, var_name)
                children_vars.append(child_var)
            
            # Generate product node code
            children = ", ".join(children_vars)
            code.append(f'        {var_name} = Product(children=[{children}])')
            
        elif isinstance(n, IdentityNumericLeaf):
            var_name = f"leaf_{node_id}"
            node_id += 1
            code.append(f'        {var_name} = IdentityNumericLeaf(mean={n.mean}, std={n.std})')
            
        elif isinstance(n, Categorical):
            var_name = f"cat_{node_id}"
            node_id += 1
            probs = ", ".join(str(p) for p in n.probs)
            code.append(f'        {var_name} = Categorical(probs=[{probs}])')
            
        else:
            raise ValueError(f"Unsupported node type: {type(n)}")
        
        node_map[id(n)] = var_name
        return var_name
    
    # Generate the root node
    root_var = generate_node_code(node, None)
    code.append(f'        return {root_var}\n')
    
    # Add likelihood and sample methods
    code.extend([
        '    def likelihood(self, data):',
        '        """Compute the likelihood of the data."""',
        '        return self.root.likelihood(data)',
        '    ', 
        '    def sample(self, n_samples=1):',
        '        """Generate samples from the model."""',
        '        return self.root.sample(n_samples)',
        '    ', 
        '    def expectation(self, ranges=None, n_samples=1000):',
        '        """Compute the expectation over the given ranges."""',
        '        from ..algorithms.expectations import expectation',
        '        return expectation(self.root, ranges, n_samples)',
    ])
    
    # Write the code to file
    with open(output_file, 'w') as f:
        f.write("\n".join(code))
    
    return output_file

def replace_template(template_path: str, replacements: Dict[str, Any]) -> str:
    """
    Replace placeholders in a template file.
    
    Args:
        template_path: Path to the template file
        replacements: Dictionary of replacements (placeholder -> value)
        
    Returns:
        The template with placeholders replaced
    """
    with open(template_path, 'r') as f:
        content = f.read()
    
    for placeholder, value in replacements.items():
        content = content.replace(f'{{{{ {placeholder} }}}}', str(value))
    
    return content
