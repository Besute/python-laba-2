from datetime import datetime

from streamstats.Errors.errors import OmitObligatoryFieldError
from streamstats.Errors.errors import WrongObligatoryCellError


class Analyzator:
    OBLIGATORY_HEADERS = ["timestamp", "level", "source", "message"]
    LEVEL_VALID = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self, data, bool_skip_invalid):
        self._data = data
        self._bool_skip_invalid = bool_skip_invalid
        warnings = None
        if bool_skip_invalid:
            warnings = []
        self.analyzed_data = {
            "all_data": 0,
            "warnings": warnings,
            self.OBLIGATORY_HEADERS[0]: [],
            self.OBLIGATORY_HEADERS[1]: [],
            self.OBLIGATORY_HEADERS[2]: [],
            self.OBLIGATORY_HEADERS[3]: [],
            "other": {},
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


class CsvAnalysis(Analyzator):

    def __init__(self, data, bool_skip_invalid):
        super().__init__(data, bool_skip_invalid)

    def analyze_csv(self):
        headers = self._data["headers"]
        data = self._data["data"]
        for file_idx in range(len(data)):
            self.check_table_headers(headers[file_idx])
            for row in range(len(data[file_idx])):
                skip = self._bool_skip_row(headers[file_idx], data[file_idx][row])
                if skip:
                    continue
                for curr_cell in range(len(data[file_idx][row])):
                    curr_cell_data = data[file_idx][row][curr_cell]
                    curr_header = headers[file_idx][curr_cell]
                    if curr_header == self.OBLIGATORY_HEADERS[0]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[0]].append(datetime.fromisoformat(curr_cell_data))
                    elif curr_header == self.OBLIGATORY_HEADERS[1]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[1]].append(curr_cell_data)
                    elif curr_header == self.OBLIGATORY_HEADERS[2]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[2]].append(curr_cell_data)
                    elif curr_header == self.OBLIGATORY_HEADERS[3]:
                        self.analyzed_data[self.OBLIGATORY_HEADERS[3]].append(curr_cell_data)
                    else:
                        self._add_new_col(curr_header)
                        self.analyzed_data["other"][curr_header].append(curr_cell_data)
        print(self.analyzed_data)
        return self.analyzed_data

    @classmethod
    def check_table_headers(cls, headers):
        was_found = {
            "timestamp": False,
            "level": False,
            "source": False,
            "message": False,
        }
        for header in headers:
            if header in cls.OBLIGATORY_HEADERS:
                was_found[header] = True
        error_fields = []
        for key in was_found.keys():
            if not was_found[key]:
                error_fields.append(key)
        if len(error_fields) > 0:
            raise OmitObligatoryFieldError(f"These fields were omit in one of your CSV table: {error_fields}")


class JsnolAnalysis(Analyzator):

    def __init__(self, data, bool_skip_invalid):
        super().__init__(data, bool_skip_invalid)

    def analyze_jsonl(self):
        data = self._data["data"]
        for file_idx in range(len(data)):
            for row in range(len(data[file_idx])):
                for key, value in data[file_idx][row].items():
                    print(key, value)
        return {}
