"""
neuro_termsets
"""
import os

__version__ = "0.1.0"

def get_config_path():
    """Return the path to the default configuration file."""
    return os.path.join(os.path.dirname(__file__), "default_config.yaml")

def load_termset_config():
    """Load the default term set configuration into PyNWB."""
    from pynwb import load_type_config
    load_type_config(config_path=get_config_path())

def get_available_termsets():
    """Return a list of available term set files."""
    term_sets_dir = os.path.join(os.path.dirname(__file__), "term_sets")
    if not os.path.exists(term_sets_dir):
        return []
    return [f for f in os.listdir(term_sets_dir) if f.endswith(".yaml")]

def get_termset_path(termset_name):
    """Return the path to a specific term set file."""
    path = os.path.join(os.path.dirname(__file__), "term_sets", termset_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Term set '{termset_name}' not found. Available term sets: {get_available_termsets()}")
    return path

def get_configured_termsets(container_class, attribute=None):
    """
    Get the configured TermSet(s) for a given PyNWB class.
    
    Args:
        container_class: A PyNWB class (e.g., Subject) or an instance of one.
        attribute (str, optional): The name of a specific attribute (e.g., 'species') to get the termset for.
            If None, returns a dictionary of all termsets configured for the class.
            
    Returns:
        TermSet or dict: If attribute is provided, returns the TermSet for that attribute.
            If attribute is None, returns a dict mapping attribute names to TermSet objects.
            
    Raises:
        ValueError: If no termset configuration is found for the class or attribute.
    """
    from pynwb import get_loaded_type_config
    from hdmf.term_set import TermSet
    
    try:
        config = get_loaded_type_config()
    except ValueError:
        # If no config is loaded yet, load the default termset config automatically
        load_termset_config()
        config = get_loaded_type_config()
        
    data_type = container_class.__name__ if isinstance(container_class, type) else type(container_class).__name__
    
    class_config = None
    # Search across all namespaces in the loaded config
    for ns_name, ns_info in config.get('namespaces', {}).items():
        if 'data_types' in ns_info and data_type in ns_info['data_types']:
            class_config = ns_info['data_types'][data_type]
            break
            
    if class_config is None:
        raise ValueError(f"No termset configuration found for class '{data_type}'.")
        
    config_base_dir = os.path.dirname(get_config_path())
    
    if attribute is not None:
        if attribute not in class_config or 'termset' not in class_config[attribute]:
            # No termset configured for attribute '{attribute}' of class '{data_type}'."
            return None
        
        relative_path = class_config[attribute]['termset']
        absolute_path = os.path.normpath(os.path.join(config_base_dir, relative_path))
        return TermSet(absolute_path)
        
    # If attribute is None, return all termsets for the class
    termsets = {}
    for attr, attr_info in class_config.items():
        if isinstance(attr_info, dict) and 'termset' in attr_info:
            relative_path = attr_info['termset']
            absolute_path = os.path.normpath(os.path.join(config_base_dir, relative_path))
            termsets[attr] = TermSet(absolute_path)
            
    return termsets

