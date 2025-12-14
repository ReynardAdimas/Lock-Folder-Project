import subprocess
import json

CONFIG_FILE = "config.json"

def load_data():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def add_folder(path):
    data = load_data()
    if path not in data["folders"]:
        data["folders"].append(path)
        save_data(data)

def remove_folder(path):
    data = load_data()
    if path in data["folders"]:
        data["folders"].remove(path)
        save_data(data)

def get_folders():
    return load_data()["folders"]

def lock_folder(path):
    subprocess.call(f'attrib +h +s "{path}"', shell=True)
    subprocess.call(f'icacls "{path}" /deny Everyone:(F)', shell=True)

def unlock_folder(path):
    subprocess.call(f'attrib -h -s "{path}"', shell=True)
    subprocess.call(f'icacls "{path}" /remove:d Everyone', shell=True)

def lock_all():
    for folder in get_folders():
        lock_folder(folder)

def unlock_all():
    for folder in get_folders():
        unlock_folder(folder)

