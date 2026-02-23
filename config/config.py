import json
import os

config_path = os.path.join(os.path.dirname(__file__), "config.json")
config_contents = open(config_path)
config = json.load(config_contents)