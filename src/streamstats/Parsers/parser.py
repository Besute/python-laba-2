from streamstats.Errors.errors import ParserError
from streamstats.EventService.csv_event import CsvEvent
from streamstats.EventService.jsonl_event import JsonlEvent

EVENTS = {}


def register_parser(name, parser_func):
    if name in EVENTS:
        raise ParserError(f"Parser already registered: {name}")

    EVENTS[name] = parser_func


def parse_csv(paths, skip_invalid=False):
    return CsvEvent(paths, skip_invalid).read()


def parse_jsonl(paths, skip_invalid=False):
    return JsonlEvent(paths, skip_invalid).read()


register_parser("csv", parse_csv)
register_parser("jsonl", parse_jsonl)
