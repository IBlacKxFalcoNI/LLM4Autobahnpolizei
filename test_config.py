import yaml

def load_config(filepath="config/config.yaml"):
    """Loads Config from YAML-File."""
    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configfile '{filepath}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error while loading config file '{filepath}': {e}")
        return None

if __name__ == "__main__":
    config = load_config()
    if config:
        autobahn_url = config.get("autobahn_api_url")
        if autobahn_url:
            print(f"The Autobahn API URL is: {autobahn_url}")
        else:
            print("The 'autobahn_api_url' was not found in the config.")