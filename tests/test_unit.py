from pathlib import Path

import awaiting_result
import pytest

from streamstats.Errors.errors import WrongObligatoryCellError
from streamstats.Errors.errors import WrongPathError
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
    assert event.analyze() == awaiting_result.CSV_RES


def test_jsonl_event():
    event = JsonlEvent([DATA_DIR / "input.jsonl"], True)
    assert event.analyze() == awaiting_result.JSONL_RES


def test_csv_event_incorrect():
    event = CsvEvent([DATA_DIR / "input.csv"], False)
    with pytest.raises(WrongObligatoryCellError):
        event.analyze()


def test_jsonl_event_incorrect():
    event = JsonlEvent([DATA_DIR / "input.jsonl"], False)
    with pytest.raises(WrongObligatoryCellError):
        event.analyze()
