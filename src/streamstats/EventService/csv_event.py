from streamstats.Parsers.json_parser import BasicJsonParser

from .base_for_event import EventSkeleton


class CsvEvent(BasicJsonParser, EventSkeleton):
    PERIOD_OF_DISPLAY = 100_000

    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid
        self._bool_big_data = []
        super().__init__()

    def read(self):
        all_headers = []
        all_data = []
        for path in self._paths:
            with open(path) as csvfile:
                if path.stat().st_size >= self.BIG_FILE_SIZE:
                    self._bool_big_data.append(True)
                else:
                    self._bool_big_data.append(False)
                acc = 0
                data = []
                headers = []
                line = csvfile.readline()
                while line:
                    data_of_line = {}
                    if acc % self.PERIOD_OF_DISPLAY == 0 and self._bool_big_data[-1]:
                        print("Total memory used during transforming data:", self.memory)
                    if acc == 0:
                        headers = line.replace("\n", "").split(",")
                    else:
                        splited_data = line.replace("\n", "").split(",")
                        for cell in range(len(headers)):
                            data_of_line[headers[cell]] = splited_data[cell]
                        data.append(data_of_line)
                    line = csvfile.readline()
                    acc += 1
            all_headers.append(headers)
            all_data.append(data)
        data_to_go = all_data
        return data_to_go, self._bool_big_data

    @property
    def big_data(self):
        return self._bool_big_data
