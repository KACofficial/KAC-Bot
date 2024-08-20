import json

def get_webui_key():
    with open("config.json") as f:
        config = json.load(f)
    return config["webui_key"]


def get_apod_key():
    with open("config.json") as f:
        config = json.load(f)
    return config["apod_key"]

