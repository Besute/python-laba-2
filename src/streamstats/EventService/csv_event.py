from streamstats.AnalyzeService.analysis import Analyzator
from streamstats.Parsers.json_parser import BasicJsonParser
from streamstats.Validation.validation import Validation


class CsvEvent(BasicJsonParser):
    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid
        self.__data_in_file = self.read_csv()

    def analyze(self):
        analyzator = Analyzator(self.__data_in_file, self._bool_skip_invalid)
        return analyzator.analyze()

    def read_csv(self):
        all_headers = []
        all_data = []
        validator = Validation()
        for path in self._paths:
            with open(path) as csvfile:
                acc = 0
                data = []
                headers = []
                line = csvfile.readline()
                while line:
                    data_of_line = {}
                    if acc == 0:
                        headers = line.replace("\n", "").split(",")
                        acc += 1
                    else:
                        splited_data = line.replace("\n", "").split(",")
                        for cell in range(len(headers)):
                            data_of_line[headers[cell]] = splited_data[cell]
                        validator.check_row_obligatory_cells(data_of_line)
                        data.append(data_of_line)
                    line = csvfile.readline()
            all_headers.append(headers)
            all_data.append(data)
        data_to_go = all_data
        return data_to_go
