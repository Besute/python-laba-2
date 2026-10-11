from streamstats.Parsers.parsers import BasicJsonParser


class ReportService(BasicJsonParser):
    BAD_ERRS = ["ERROR", "CRITICAL"]

    def __init__(self, data):
        self._data = self.from_json(data)
        self._data["top_errors"] = self.__make_top_of_errors()

    def __make_top_of_errors(self):
        acc_of_sources = {}
        set_of_sources = set()
        print(self._data)
        for i in range(len(self._data["level"])):
            err = self._data["level"][i]
            if err in self.BAD_ERRS:
                if err not in acc_of_sources:
                    acc_of_sources[err] = 0
                acc_of_sources[err] += 1
                set_of_sources.add(err)
        sorted_arr_of_sources = sorted(acc_of_sources.items(), key=lambda x: acc_of_sources[x])
        print(sorted_arr_of_sources)
        return sorted_arr_of_sources
