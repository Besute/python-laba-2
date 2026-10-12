class Validation:
    OBLIGATORY_HEADERS = ["timestamp", "level", "source", "message"]

    def __init__(self):
        self.__invalid_files = []

    def check_rows_obligatory_cells(self, rows):
        if len(rows) == 0:
            was_found = {
                "timestamp": False,
                "level": False,
                "source": False,
                "message": False,
            }
            error_fields = []
            for key in was_found.keys():
                if not was_found[key]:
                    error_fields.append(key)
            self.__invalid_files.append(error_fields)
            return True
        for row in rows:
            was_found = {
                "timestamp": False,
                "level": False,
                "source": False,
                "message": False,
            }
            for key, item in row.items():
                if key == "timestamp":
                    was_found["timestamp"] = True
                elif key == "level":
                    was_found["level"] = True
                elif key == "source":
                    was_found["source"] = True
                elif key == "message":
                    was_found["message"] = True
            error_fields = []
            for key in was_found.keys():
                if not was_found[key]:
                    error_fields.append(key)
            if len(error_fields) > 0:
                self.__invalid_files.append(error_fields)
                return True
        return False

    @property
    def invalid_files(self):
        return self.__invalid_files
