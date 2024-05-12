import yaml, os

def safe_load_config(config_path) -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
    
def load_config() -> dict:
    this_dir = os.path.dirname(__file__)
    if os.path.exists(os.path.join(this_dir, 'protected_config.yaml')):
        return safe_load_config(os.path.join(this_dir, 'protected_config.yaml'))
    else:
        return safe_load_config(os.path.join(this_dir, 'config.yaml'))


if __name__ == '__main__':
    print(load_config())