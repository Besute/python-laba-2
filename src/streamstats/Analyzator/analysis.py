class AnalysisCsv:
    def __init__(self, data):
        self.__data = data

    def analyze_csv(self):
        headers = self.__data["headers"]
        data = self.__data["data"]
        for i in range(len(headers)):
            for j in range(len(data)):
                if headers[i][j] == "":
                    pass
        return {}


class AnalysisJsonl:
    def __init__(self, data):
        self.__data = data

    def analyze_jsonl(self):
        print(f"Json analyzed {self.__data}")
        return {}


class Analyzator(AnalysisCsv, AnalysisJsonl):
    oblig_fields = ["timestamp", "level", "source", "message"]

    def __init__(self, data, bool_skip_invalid):
        super().__init__(data)
        self._bool_skip_invalid = bool_skip_invalid

    @classmethod
    def check_table_headers(cls, headers):
        was_found = {
            "timestamp": False,
            "level": False,
            "source": False,
            "message": False,
        }
        for header in headers:
            if header in cls.oblig_fields:
                was_found["timestamp"] = True
        error_fields = []
        for key in was_found.keys():
            if not was_found[key]:
                error_fields.append(key)

        return error_fields
