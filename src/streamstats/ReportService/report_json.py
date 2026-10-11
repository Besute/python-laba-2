class JsonReport:
    def __init__(self, data):
        self._all_data = data["allData"]
        self._warnings = data["warnings"]
        self._errors = data["errors"]
