from datetime import datetime

from streamstats.Errors.errors import InvalidValueError
from streamstats.Errors.errors import WrongObligatoryCellError
from streamstats.MemoryCounter.memory_count import CreateVirtualMemory


class Analyzator:
    OBLIGATORY_HEADERS = ("timestamp", "level", "source", "message")
    LEVEL_VALID = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    def __init__(self, bool_skip_invalid, bool_big_data):
        self._bool_skip_invalid = bool_skip_invalid
        self.__bool_big_data = bool_big_data
        warnings = None
        if bool_skip_invalid:
            warnings = []
        self.analyzed_data = {
            self.OBLIGATORY_HEADERS[0]: [],
            self.OBLIGATORY_HEADERS[1]: [],
            self.OBLIGATORY_HEADERS[2]: [],
            self.OBLIGATORY_HEADERS[3]: [],
            "other": {},
            "all_data": 0,
            "warnings": warnings,
            "acc_of_every_source": {},
            "acc_of_every_level": {},
            "minmax_date": (),
        }

    def _add_new_col(self, name):
        if name not in self.analyzed_data["other"]:
            self.analyzed_data["other"][name] = []

    def _bool_skip_row(self, data, file_idx):
        bool_wrong = False
        for key, value in data.items():
            if key == self.OBLIGATORY_HEADERS[0]:
                try:
                    datetime.fromisoformat(value)
                except ValueError:
                    bool_wrong = True
            elif key == self.OBLIGATORY_HEADERS[1]:
                if value not in self.LEVEL_VALID:
                    bool_wrong = True
            elif key == self.OBLIGATORY_HEADERS[2]:
                if len(value.replace(" ", "")) == 0 or type(value) is not str:
                    bool_wrong = True
            elif key == self.OBLIGATORY_HEADERS[3] and type(value) is not str:
                bool_wrong = True
            if bool_wrong and not self._bool_skip_invalid:
                raise WrongObligatoryCellError(
                    f"File №{file_idx + 1}! The stroke in '{key}' column has wrong type! (Now there: '{value}')"
                )
            elif bool_wrong:
                self.analyzed_data["warnings"].append(
                    f"File №{file_idx + 1}! WARNING: obligatory col '{key}' has invalid format: '{value}'"
                )
                return True
        return False

    def analyze(self, data):
        for file_idx in range(len(data)):
            bool_file_big = self.__bool_big_data[file_idx]
            memory_counter = None
            if bool_file_big:
                memory_counter = CreateVirtualMemory()
            for row in range(len(data[file_idx])):
                if row % 10000 == 0 and memory_counter is not None:
                    print("Total memory used during analization:", memory_counter.memory)
                self.analyzed_data["all_data"] += 1
                skip = self._bool_skip_row(data[file_idx][row], file_idx)
                if skip:
                    continue
                for key, value in data[file_idx][row].items():
                    if key == self.OBLIGATORY_HEADERS[0]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[0]].append(value)
                    elif key == self.OBLIGATORY_HEADERS[1]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[1]].append(value)
                        if value not in self.analyzed_data["acc_of_every_level"]:
                            self.analyzed_data["acc_of_every_level"][value] = 0
                        self.analyzed_data["acc_of_every_level"][value] += 1
                    elif key == self.OBLIGATORY_HEADERS[2]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[2]].append(value)
                        if value not in self.analyzed_data["acc_of_every_source"]:
                            self.analyzed_data["acc_of_every_source"][value] = 0
                        self.analyzed_data["acc_of_every_source"][value] += 1
                    elif key == self.OBLIGATORY_HEADERS[3]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[3]].append(value)
                    else:
                        self._add_new_col(key)
                        self.analyzed_data["other"][key].append(value)
        correct_date = list(map(datetime.fromisoformat, self.analyzed_data["timestamp"]))
        if len(correct_date) == 0:
            raise InvalidValueError("There is no valid data in your files")
        self.analyzed_data["minmax_date"] = min(correct_date).isoformat(), max(correct_date).isoformat()
        return self.analyzed_data
