from datetime import datetime

from streamstats.Errors.errors import WrongObligatoryCellError


class Analyzator:
    OBLIGATORY_HEADERS = ["timestamp", "level", "source", "message"]
    LEVEL_VALID = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self, bool_skip_invalid):
        self._bool_skip_invalid = bool_skip_invalid
        warnings = None
        if bool_skip_invalid:
            warnings = []
        self.analyzed_data = {
            self.OBLIGATORY_HEADERS[0]: [],
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

    def _bool_skip_row(self, header, data):
        bool_wrong = False
        if len(header) != len(data):
            bool_wrong = True
        for cell in range(len(header)):
            if header[cell] == self.OBLIGATORY_HEADERS[0]:
                try:
                    datetime.fromisoformat(data[cell])
                except ValueError:
                    bool_wrong = True
            elif header[cell] == self.OBLIGATORY_HEADERS[1]:
                if data[cell] not in self.LEVEL_VALID:
                    bool_wrong = True
            elif header[cell] == self.OBLIGATORY_HEADERS[2]:
                if len(data[cell].replace(" ", "")) == 0 or type(data[cell]) is not str:
                    bool_wrong = True
            elif header[cell] == self.OBLIGATORY_HEADERS[3]:
                if type(data[cell]) is not str:
                    bool_wrong = True
            if bool_wrong and not self._bool_skip_invalid:
                raise WrongObligatoryCellError(
                    f"The stroke in '{header[cell]}' column has wrong type! (Now there: '{data[cell]}')"
                )
            elif bool_wrong:
                self.analyzed_data["warnings"].append(
                    f"WARNING: obligatory col '{header[cell]}' has invalid format: '{data[cell]}'"
                )
                return True
        return False

    def analyze(self, data):
        for file_idx in range(len(data)):
            for row in range(len(data[file_idx])):
                self.analyzed_data["all_data"] += 1
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
        self.analyzed_data["minmax_date"] = min(correct_date).isoformat(), max(correct_date).isoformat()
        return self.analyzed_data
