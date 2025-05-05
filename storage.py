import json
from datetime import datetime

def save_result(score, total, accuracy, op, diff, time_taken):
    # create the result dict with all the info we need
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "total": total,
        "accuracy": accuracy,  # this is a string like "80.0"
        "operation": op,
        "difficulty": diff,
        "time_taken": time_taken
    }

    path = "data/score_history.json"

    # load old results
    with open(path, "r") as f:
        history = json.load(f)

    # add this new one
    history.append(result)

    # write everything back
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

    return

def load_history():
    path = "data/score_history.json"

    # open and return the data
    with open(path, "r") as f:
        return json.load(f)
