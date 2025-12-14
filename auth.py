import hashlib
import json
import os

CONFIG_FILE = "config.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_config():
    if not os.path.exists(CONFIG_FILE):
        data = {
            "password": hash_password("admin"),
            "folders": []
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

def verify_password(password):
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return hash_password(password) == data["password"]

