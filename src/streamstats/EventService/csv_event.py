class CsvEvent:

    @classmethod
    def read_csv(cls, paths):
        all_headers = []
        all_data = []
        for path in paths:
            with open(path) as csvfile:
                acc = 0
                data = []
                headers = []
                line = csvfile.readline()
                while line:
                    if acc == 0:
                        headers = line.replace("\n", "").split(",")
                        acc += 1
                    else:
                        data.append(line.replace("\n", "").split(","))
                    line = csvfile.readline()
            all_headers.append(headers)
            all_data.append(data)
        data_to_go = {"headers": all_headers, "data": all_data}
        return data_to_go
