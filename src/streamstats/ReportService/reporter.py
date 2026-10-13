from streamstats.Parsers.json_parser import BasicJsonParser

from .report_csv import CsvReport
from .report_json import JsonReport


class ReportService(BasicJsonParser):
    BAD_ERRS = ["ERROR", "CRITICAL"]

    def __init__(self, data):
        self._data = data
        self._data["rating_top_errors"] = self.__make_top_of_errors()
        self._handlers = {"csv": self._csv_report, "json": self._json_report}

    def __make_top_of_errors(self):
        acc_of_sources = {}
        set_of_sources = set()
        for i in range(len(self._data["level"])):
            level = self._data["level"][i]
            source = self._data["source"][i]
            if level in self.BAD_ERRS:
                if source not in acc_of_sources:
                    acc_of_sources[source] = 0
                acc_of_sources[source] += 1
                set_of_sources.add(source)
        sorted_arr_of_sources = sorted(set_of_sources, key=lambda src_: -acc_of_sources[src_])[:5]
        return sorted_arr_of_sources

    def __write_data(self):
        data_to_write = {}
        data_to_write["Total events"] = self._data["all_data"]
        data_to_write["Minimum time"] = self._data["minmax_date"][0]
        data_to_write["Maximum time"] = self._data["minmax_date"][1]
        data_to_write["All warnings"] = self._data["warnings"]
        data_to_write["Number of events from all sources"] = self._data["acc_of_every_source"]
        data_to_write["Number of events from all levels"] = self._data["acc_of_every_level"]
        data_to_write["TOP 5 sources by number of errors"] = self._data["rating_top_errors"]
        return data_to_write

    def make_report(self, output: str):
        output_extension = output.split(".")[-1]
        handler = self._handlers[output_extension]
        return handler(output, self.__write_data())

    @classmethod
    def _json_report(cls, output: str, data: dict):
        json_reporter = JsonReport(data, output)
        json_reporter.write_output_file()

    @classmethod
    def _csv_report(cls, output: str, data: dict):
        csv_reporter = CsvReport(data, output)
        csv_reporter.write_output_file()
