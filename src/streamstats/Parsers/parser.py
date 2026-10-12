from streamstats.EventService.csv_event import CsvEvent
from streamstats.EventService.jsonl_event import JsonlEvent

CURRENT_EVENTS = {}


def register_parser(name, parser_func):
    if name in CURRENT_EVENTS:
        raise ValueError(f"Parser already registered: {name}")

    CURRENT_EVENTS[name] = parser_func


def parse_csv(paths, skip_invalid=False):
    return CsvEvent(paths, skip_invalid).analyze()


def parse_jsonl(paths, skip_invalid=False):
    return JsonlEvent(paths, skip_invalid).analyze()


register_parser("csv", parse_csv)
register_parser("jsonl", parse_jsonl)
