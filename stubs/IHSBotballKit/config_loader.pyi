def load_json(json_file_path: str) -> dict:
    """Load configurations from a json file.

    Args:
        json_file_path (str): File path of the json file. Absolute path is preferred over relative path.

    Returns:
        configs (dict): A dictionary with the json values as key-value pairs.
    """
def inject_namespace(namespace: dict, dictionary: dict) -> None:
    """Inject the key-value pairs from a dictionary into a namespace as variables.

    Args:
        namespace (dict): The namespace to inject into. For the global namespace, use `globals()`.
        configuration_dict (dict): The dictionary to use. 
    """
