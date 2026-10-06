class CsvEvent:

    @classmethod
    def read_csv(cls, path):
        with open(path) as csvfile:
            for line in csvfile.readlines():
                print(line)
