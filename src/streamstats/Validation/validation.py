from streamstats.Errors.errors import OmitObligatoryFieldError


class Validation:
    OBLIGATORY_HEADERS = ["timestamp", "level", "source", "message"]

    @classmethod
    def check_row_obligatory_cells(cls, row):
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
            raise OmitObligatoryFieldError(f"These fields were omit in one of your CSV rows: {error_fields}")
