import csv

from pathlib import Path

from .base_for_report import ReportSkeleton


class CsvReport(ReportSkeleton):

    def __init__(self, data, output):
        self._data = data
        self.__output_path = Path(__file__).resolve().parent.parent.joinpath(output)
        self._filename = output

    def create_file(self):
        idx_of_first_slash = self._filename.rfind("/")
        if idx_of_first_slash != -1:
            path_no_file = self._filename[:idx_of_first_slash]
            path_of_outputdir = Path(__file__).resolve().parent.parent.joinpath(path_no_file)
            if not path_of_outputdir.exists():
                path_of_outputdir.mkdir(parents=True, exist_ok=True)
        if not self.__output_path.exists():
            self.__output_path.touch()

    def write_output_file(self):
        self.create_file()
        with open(self.__output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "value"])
            for key, value in self._data.items():
                writer.writerow([key, value])
