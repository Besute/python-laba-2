from streamstats.Parsers.parsers import BasicJsonParser


class ReportService(BasicJsonParser):
    BAD_ERRS = ["ERROR", "CRITICAL"]

    def __init__(self, data):
        self._data = data
        self._data["top_errors"] = self.__make_top_of_errors()

    def __make_top_of_errors(self):
        acc_of_sources = {}
        set_of_sources = set()
        for i in range(len(self._data["level"])):
            level = self._data["level"][i]
            source = self._data["source"][i]
            if level in self.BAD_ERRS:
                if source not in acc_of_sources:
                    acc_of_sources[source] = 0
                acc_of_sources[source] += 1
                set_of_sources.add(source)
        sorted_arr_of_sources = sorted(set_of_sources, key=lambda x: -acc_of_sources[x])[:5]
        return sorted_arr_of_sources
