from asyncio import sleep
from pathlib import Path

from streamstats.Errors.errors import InvalidExtensionError
from streamstats.Errors.errors import InvalidMethodError
from streamstats.Errors.errors import InvalidValueError
from streamstats.Errors.errors import WrongPathError
from streamstats.EventService.create_event import EventService
from streamstats.Parsers.json_parser import BasicJsonParser
from streamstats.ReportService.reporter import ReportService
from streamstats.Validation.validation import Validation


class Server(BasicJsonParser):
    VALID_TYPES = ["csv", "jsonl"]

    def __init__(self, output):
        self.output = output
        self._handlers = {
            "GET": self.__method_get,
            "POST": self.__method_post,
        }

    async def make_request(self, request):
        normal_data = self.from_json(request.curr_json)
        return await self.__verify_handler(request.method, normal_data)

    async def __verify_handler(self, method, data=None):
        handler = self._handlers.get(method)
        if handler is None:
            raise InvalidMethodError(f"Invalid method {method}")
        if data is None:
            raise InvalidValueError("Invalid data")

        if method == "GET":
            self._check_valid_type(data["type"])
            data["path"] = self._check_correct_filepath(data["path"], data["type"])
        else:
            data["output"] = self.output
        res = handler(data)
        await sleep(0)
        return res

    @classmethod
    def __method_get(cls, data):
        event = EventService(data)
        valid_files = []
        validator = Validation()
        for file in event.data_good_format:
            bool_invalid = validator.check_rows_obligatory_cells(file)
            if bool_invalid:
                continue
            valid_files.append(file)
        if len(validator.invalid_files) == len(data["path"]):
            raise InvalidValueError("You doesn't have valid files")
        elif len(validator.invalid_files):
            print(
                f"Warning: in some of your files were omit these headers: {validator.invalid_files}, "
                f"so some files weren't analyzed"
            )
        return event.analyze(valid_files)

    @classmethod
    def __method_post(cls, data):
        reporter = ReportService(data["data"])
        idx_of_extension = data["output"].rfind(".")
        output_no_extension = data["output"][:idx_of_extension]
        reporter.make_report(output_no_extension + ".json")
        reporter.make_report(output_no_extension + ".csv")

    @classmethod
    def _check_valid_type(cls, value):
        if value not in cls.VALID_TYPES:
            raise InvalidValueError(f"Invalid value {value}. Must be one of {cls.VALID_TYPES}")
        return value

    @classmethod
    def _check_correct_filepath(cls, value, type_):
        correct_files = []
        curr_path = Path(__file__).resolve().parent.parent

        for file in value:
            curr_file = curr_path / file
            extension = file.split(".")[-1]
            if extension.lower() != type_.lower():
                raise InvalidExtensionError(
                    f"Invalid file extension: expected {type_}, " f"but got {extension or 'no extension'}"
                )
            if not curr_file.is_file():
                raise WrongPathError(f"Invalid filepath {file}. File does not exist")
            correct_files.append(curr_file)
        return correct_files
