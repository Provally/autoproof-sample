import yaml


def load_mapping(text):
    """Read the column mapping (mapping.yaml) that comes inside each partner bundle."""
    return yaml.load(text, Loader=yaml.Loader)
