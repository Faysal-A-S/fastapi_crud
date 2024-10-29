import json
import os


DATABASE_FOLDER = "src/database"
FILE_PATH = os.path.join(DATABASE_FOLDER, "data.json")


if not os.path.exists(DATABASE_FOLDER):
    os.makedirs(DATABASE_FOLDER)
def read_json_file():
    if not os.path.exists(FILE_PATH):
        print("File does not exist, returning empty list.")
        write_json_file([])
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def write_json_file(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)