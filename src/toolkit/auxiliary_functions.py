import json

from .constants import OPERANDS


def save_data(data, path):
    """Creates new file and writes data to it"""
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def is_int(num):
    return int(num) == num


def is_oper(symb):
    return symb in OPERANDS


def load_data(path):
    with open(path, "r") as file:
        return json.load(file)


def save_history(data, path):
    """Loads previous data and saves it with new one"""
    current_data = []
    if path.is_file():
        current_data = load_data(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    current_data.append(data)
    path.write_text(
        json.dumps(current_data[::-1], indent=1) + "\n",
        encoding="utf-8",
    )
