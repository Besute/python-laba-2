from pathlib import Path

class Server:
    VALID_TYPES = ["csv", "jsonl"]

    def __init__(self, path, type_, output, skip_invalid):
        self._path = self.check_correct_filepath(path)
        self._type = self.check_valid_type(type_)
        self._output = output
        self._skip_invalid = skip_invalid
        self.__make_csv_event = self.bool_can_make_event("csv", type_)
        self.__make_jsonl_event = self.bool_can_make_event("jsonl", type_)

    # def make_jsonl_event(self):
    #     if not self.__make_jsonl_event:
    #         # TODO: normal Error
    #         raise ValueError("You can't open this file with jsonl")
    #     pass
    #
    # def make_csv_event(self):
    #     if not self.__make_csv_event:
    #         # TODO: normal Error
    #         raise ValueError("You can't open this file with csv")

    @classmethod
    def bool_can_make_event(cls, value_goal, value_curr):
        return value_goal == value_curr

    @classmethod
    def check_valid_type(cls, value):
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid value {value}. Must be one of {cls.VALID_TYPES}")
        return value

    @classmethod
    def check_correct_filepath(cls, value):
        if not Path(value).is_file():
            raise ValueError(f"Invalid filepath {value}. File does not exist")
        return value
