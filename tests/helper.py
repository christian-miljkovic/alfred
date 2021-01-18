from pathlib import Path
import json


def setup_fixture_object(file_path):
    fixture_data_folder = Path().cwd() / Path("tests/fixtures")
    fixture_data_file = fixture_data_folder / str(file_path)
    with open(fixture_data_file) as json_file:
        return json.load(json_file)
