import json

from pathlib import Path


class JsonReport:
    def __init__(self, data, output):
        self._data = data
        self.__output_path = Path(__file__).resolve().parent.parent.joinpath("output/" + output)
        self._filename = output
        self.create_file()

    def create_file(self):
        if not self.__output_path.exists():
            self.__output_path.touch()

    def write_output_file(self):
        self.create_file()
        print("HERE")
        with open(self.__output_path, "w") as file:
            json.dump(self._data, file, indent=4)
