from streamstats.AnalyzeService.analysis import JsnolAnalysis
from streamstats.Parsers.parsers import BasicJsonParser


class JsonlEvent(BasicJsonParser):

    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid
        self.__data_in_file = self.read_jsonl()

    def analyze(self):
        analyzator = JsnolAnalysis(self.__data_in_file, self._bool_skip_invalid)
        return analyzator.analyze_jsonl()

    def read_jsonl(self):
        final_data = []
        for path in self._paths:
            with open(path) as jsonfile:
                line = jsonfile.readline()
                data_of_file = []
                while line:
                    line = self.from_json(line)
                    data_of_file.append(line)
                    line = jsonfile.readline()
                final_data.append(data_of_file)
        data_to_go = {"headers": None, "data": final_data}
        return data_to_go

    @property
    def data_in_file(self):
        return self.__data_in_file

    @data_in_file.setter
    def data_in_file(self, val):
        self.__data_in_file = val
