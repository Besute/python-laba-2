class AnalysisCsv:
    @classmethod
    def analyze(cls, data):
        print("Csv analyzed")


class AnalysisJson:
    @classmethod
    def analyze(cls, data):
        print("Json analyzed")


class Analysis(AnalysisCsv, AnalysisJson):
    def __init__(self, data):
        self.data = data


def analysis(data):
    Analysis.analyze(data)
