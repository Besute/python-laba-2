from streamstats.AnalyzeService.analysis import CsvAnalysis
from streamstats.Parsers.json_parser import BasicJsonParser


class CsvEvent(BasicJsonParser):
    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid
        self.__data_in_file = self.read_csv()

    def analyze(self):
        analyzator = CsvAnalysis(self.__data_in_file, self._bool_skip_invalid)
        return analyzator.analyze_csv()

    def read_csv(self):
        all_headers = []
        all_data = []
        for path in self._paths:
            with open(path) as csvfile:
                acc = 0
                data = []
                headers = []
                line = csvfile.readline()
                while line:
                    if acc == 0:
                        headers = line.replace("\n", "").split(",")
                        acc += 1
                    else:
                        data.append(line.replace("\n", "").split(","))
                    line = csvfile.readline()
            all_headers.append(headers)
            all_data.append(data)
        data_to_go = {"headers": all_headers, "data": all_data}
        return data_to_go
