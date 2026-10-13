from streamstats.Parsers.json_parser import BasicJsonParser

from .base_for_event import EventSkeleton


class CsvEvent(BasicJsonParser, EventSkeleton):
    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid

    def read(self):
        all_headers = []
        all_data = []
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
                        data.append(data_of_line)
                    line = csvfile.readline()
            all_headers.append(headers)
            all_data.append(data)
        data_to_go = all_data
        return data_to_go
