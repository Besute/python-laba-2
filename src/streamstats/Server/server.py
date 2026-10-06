from asyncio import sleep
from pathlib import Path

from streamstats.EventService.create_event import EventService
from streamstats.parsers import BasicJsonParser


class Server(BasicJsonParser):
    VALID_TYPES = ["csv", "jsonl"]
    answer = None

    def __init__(self):
        self.handlers = {
            "GET": self.method_get,
            "POST": self.method_post,
        }

    async def make_request(self, request):
        normal_data = self.from_json(request.curr_json)
        await self.verify_handler(request.method, normal_data)

    async def verify_handler(self, method, data=None):
        handler = self.handlers.get(method)

        if handler is None:
            raise ValueError(f"Invalid method {method}")
        if data is None:
            raise ValueError("Invalid data")

        self.check_valid_type(data["type"])
        data["path"] = self.check_correct_filepath(data["path"])

        res = handler(data)
        await sleep(0)
        return res

    def method_get(self, data):
        return data

    def method_post(self, data):
        event = EventService(data)
        print(event)

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

    # @classmethod
    # def bool_can_make_event(cls, value_goal, value_curr):
    #     return value_goal == value_curr

    @classmethod
    def check_valid_type(cls, value):
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid value {value}. Must be one of {cls.VALID_TYPES}")
        return value

    @classmethod
    def check_correct_filepath(cls, value):
        curr_path = Path(__file__).resolve().parent.parent
        curr_file = curr_path / value[0]
        if not curr_file.is_file():
            raise ValueError(f"Invalid filepath {value}. File does not exist")
        return curr_file
