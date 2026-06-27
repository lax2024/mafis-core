import json
import os


def save_log(result):
    filename = "logs.json"

    # if file missing or corrupted
    if not os.path.exists(filename):
        logs = []
    else:
        try:
            with open(filename, "r") as f:
                logs = json.load(f)
        except:
            logs = []

    logs.append(result)

    with open(filename, "w") as f:
        json.dump(logs, f, indent=4, default=str)