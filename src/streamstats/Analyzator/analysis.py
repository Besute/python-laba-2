from streamstats.Errors.errors import OmitObligatoryFieldError


class Analyzator:

    def __init__(self, data, bool_skip_invalid):
        self._data = data
        self._bool_skip_invalid = bool_skip_invalid


class CsvAnalysis(Analyzator):
    OBLIGATORY_HEADERS = ["timestamp", "level", "source", "message"]

    def __init__(self, data, bool_skip_invalid):
        super().__init__(data, bool_skip_invalid)

    def analyze_csv(self):
        headers = self._data["headers"]
        data = self._data["data"]
        for i in range(len(data)):
            self.check_table_headers(headers[i])
            for j in range(len(data)):
                if headers[i][j] == "":
                    pass
        return {}

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
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j] == "":
                    pass
        return {}
