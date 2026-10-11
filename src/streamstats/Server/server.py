import re

from asyncio import sleep
from pathlib import Path

from streamstats.EventService.create_event import EventService
from streamstats.Parsers.parsers import BasicJsonParser
from streamstats.ReportService.reporter import ReportService


class Server(BasicJsonParser):
    VALID_TYPES = ["csv", "jsonl"]
    curr_id = 1
    answers = {}

    def __init__(self):
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
            raise ValueError(f"Invalid method {method}")
        if data is None:
            raise ValueError("Invalid data")

        if method == "GET":
            self._check_valid_type(data["type"])
            data["path"] = self._check_correct_filepath(data["path"], data["type"])

        res = handler(data)
        await sleep(0)
        return res

    @classmethod
    def __method_get(cls, data):
        event = EventService(data)
        event.create_event()
        return event.analyzed_data

    @classmethod
    def __method_post(cls, data):
        reporter = ReportService(data["data"])
        print(reporter._data)

    @classmethod
    def _check_valid_type(cls, value):
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid value {value}. Must be one of {cls.VALID_TYPES}")
        return value

    @classmethod
    def _check_correct_filepath(cls, value, type_):
        correct_files = []
        mask = "\\.[a-zA-Z]*"

        for file in value:
            curr_path = Path(__file__).resolve().parent.parent
            curr_file = curr_path / file
            after_dot = re.search(mask, file).group().replace(".", "")
            if after_dot != type_:
                raise ValueError(f"Invalid file extension: you have {type_}, but you need {after_dot}")
            if not curr_file.is_file():
                raise ValueError(f"Invalid filepath {file}. File does not exist")
            correct_files.append(curr_file)
        return correct_files
