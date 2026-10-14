from pathlib import Path

import awaiting_result
import pytest

from streamstats.AnalyzeService.analysis import Analyzator
from streamstats.Errors.errors import InvalidValueError
from streamstats.Errors.errors import WrongObligatoryCellError
from streamstats.Errors.errors import WrongPathError
from streamstats.EventService.create_event import EventService
from streamstats.EventService.csv_event import CsvEvent
from streamstats.EventService.jsonl_event import JsonlEvent
from streamstats.Server.server import Server
from streamstats.__main__ import GetJson
from streamstats.__main__ import PostJson

DATA_DIR = Path(__file__).parent / "data"


def test_get_request():
    data = {
        "username": "test",
        "password": "",
    }
    goal_data = ("GET", '{"username": "test", "password": ""}')
    assert GetJson(data).curr_json == goal_data[1]
    assert GetJson(data).method == goal_data[0]


def test_post_request():
    data = {
        "username": "test",
        "password": "",
    }
    goal_data = ("POST", '{"username": "test", "password": ""}')
    assert PostJson(data).curr_json == goal_data[1]
    assert PostJson(data).method == goal_data[0]


@pytest.mark.asyncio
async def test_server_get_request_unexisting_file():
    get_request = GetJson(
        {
            "path": [str(DATA_DIR / "AAA.csv")],
            "type": "csv",
            "skipInvalid": "true",
        }
    )
    server = Server("123.json")
    with pytest.raises(WrongPathError):
        await server.make_request(get_request)


def test_csv_event():
    event = CsvEvent([DATA_DIR / "input.csv"], True)
    assert event.read() == awaiting_result.CSV_RES


def test_jsonl_event():
    event = JsonlEvent([DATA_DIR / "input.jsonl"], True)
    assert event.read() == awaiting_result.JSONL_RES


def test_csv_event_incorrect():
    data = {
        "path": [str(DATA_DIR / "input.csv")],
        "skipInvalid": "false",
        "type": "csv",
    }
    event = EventService(data)
    analyzator = Analyzator(False, [False])
    with pytest.raises(WrongObligatoryCellError):
        analyzator.analyze(event.data_good_format)


def test_jsonl_event_incorrect():
    data = {
        "path": [str(DATA_DIR / "input.jsonl")],
        "skipInvalid": "false",
        "type": "jsonl",
    }
    event = EventService(data)
    analyzator = Analyzator(False, [False])
    with pytest.raises(WrongObligatoryCellError):
        analyzator.analyze(event.data_good_format)


@pytest.mark.asyncio
async def test_empty_jsonl():
    data = {
        "path": [str(DATA_DIR / "empty.jsonl")],
        "skipInvalid": False,
        "type": "jsonl",
    }
    server = Server("1111.txt")
    with pytest.raises(InvalidValueError):
        await server.make_request(GetJson(data))


@pytest.mark.asyncio
async def test_empty_csv():
    data = {
        "path": [str(DATA_DIR / "empty.csv")],
        "skipInvalid": False,
        "type": "csv",
    }
    server = Server("1111.txt")
    with pytest.raises(InvalidValueError):
        await server.make_request(GetJson(data))


@pytest.mark.asyncio
async def test_incorrect_cell_csv():
    data = {
        "path": [str(DATA_DIR / "incorrect_cell.csv")],
        "skipInvalid": False,
        "type": "csv",
    }
    server = Server("1111.txt")
    with pytest.raises(WrongObligatoryCellError):
        await server.make_request(GetJson(data))


@pytest.mark.asyncio
async def test_incorrect_cell_jsonl():
    data = {
        "path": [str(DATA_DIR / "incorrect_cell.jsonl")],
        "skipInvalid": False,
        "type": "jsonl",
    }
    server = Server("1111.txt")
    with pytest.raises(WrongObligatoryCellError):
        await server.make_request(GetJson(data))
