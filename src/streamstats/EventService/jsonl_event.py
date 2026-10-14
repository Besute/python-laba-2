from streamstats.Parsers.json_parser import BasicJsonParser

from .base_for_event import EventSkeleton


class JsonlEvent(BasicJsonParser, EventSkeleton):
    PERIOD_OF_DISPLAY = 100_000

    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid
        self._bool_big_data = []
        super().__init__()

    def read(self):
        final_data = []
        for path in self._paths:
            with open(path) as jsonfile:
                if path.stat().st_size >= self.BIG_FILE_SIZE:
                    self._bool_big_data.append(True)
                else:
                    self._bool_big_data.append(False)
                line = jsonfile.readline()
                data_of_file = []
                acc = 0
                while line:
                    if acc % self.PERIOD_OF_DISPLAY == 0 and self._bool_big_data[-1]:
                        print("Total memory used during transforming data:", self.memory)
                    line = self.from_json(line)
                    data_of_file.append(line)
                    line = jsonfile.readline()
                    acc += 1
                final_data.append(data_of_file)
        data_to_go = final_data
        return data_to_go, self._bool_big_data

    @property
    def big_data(self):
        return self._bool_big_data
