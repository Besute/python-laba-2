from streamstats.parsers import BasicJsonParser


class JsonlEvent(BasicJsonParser):

    def read_jsonl(self, paths):
        final_data = []
        for path in paths:
            with open(path) as jsonfile:
                line = jsonfile.readline()
                data_of_file = []
                while line:
                    data = self.from_json(line)
                    data_of_file.append(data)
                    line = jsonfile.readline()
                final_data.append(data_of_file)
        data_to_go = {"Headers": None, "Data": final_data}
        return data_to_go
