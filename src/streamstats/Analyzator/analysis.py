class AnalysisCsv:
    def __init__(self, data):
        self.__data = data

    def analyze_csv(self):
        print(f"Csv analyzed {self.__data}")
        return {}


class AnalysisJsonl:
    def __init__(self, data):
        self.__data = data

    def analyze_jsonl(self):
        print(f"Json analyzed {self.__data}")
        return {}


class Analyzator(AnalysisCsv, AnalysisJsonl):
    def __init__(self, data):
        super().__init__(data)
