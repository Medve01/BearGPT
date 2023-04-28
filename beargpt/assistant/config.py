import json

# Read the configuration from the config.json file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

def config(key):
    """Return the configuration value for the given key."""
    return config_data.get(key)
