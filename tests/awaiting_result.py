JSONL_RES = {
    "timestamp": ["2026-10-11T14:30:00Z"],
    "level": ["DEBUG"],
    "source": [" 123"],
    "message": ["Hello"],
    "other": {"C6": ["RRRRR"]},
    "all_data": 1,
    "warnings": ["WARNING: obligatory col 'level' has invalid format: 'DEBUGG'"],
    "acc_of_every_source": {" 123": 1},
    "acc_of_every_level": {"DEBUG": 1},
    "minmax_date": ("2026-10-11T14:30:00+00:00", "2026-10-11T14:30:00+00:00"),
}
CSV_RES = {
    "timestamp": ["2023-10-11T14:30:00Z"],
    "level": ["ERROR"],
    "source": ["SOURCE_1"],
    "message": ["Four"],
    "other": {},
    "all_data": 1,
    "warnings": [
        "WARNING: obligatory col 'timestamp' has invalid format: 'timestamp'",
        "WARNING: obligatory col 'timestamp' has invalid format: 'timestamp'",
    ],
    "acc_of_every_source": {"SOURCE_1": 1},
    "acc_of_every_level": {"ERROR": 1},
    "minmax_date": ("2023-10-11T14:30:00+00:00", "2023-10-11T14:30:00+00:00"),
}

REPORT_JSONL = {
    "Total events": 2,
    "Minimum time": "2026-10-11T14:30:00+00:00",
    "Maximum time": "2026-10-11T14:30:00+00:00",
    "All warnings": [
        "WARNING: obligatory col 'level' has invalid format: 'DEBUGG'",
        "WARNING: obligatory col 'level' has invalid format: 'DEBUGG'",
    ],
    "Number of events from all sources": {" 123": 2},
    "Number of events from all levels": {"DEBUG": 2},
    "TOP 5 sources by number of errors": [],
}

REPORT_CSV = {
    "Total events": 1,
    "Minimum time": "2023-10-11T14:30:00+00:00",
    "Maximum time": "2023-10-11T14:30:00+00:00",
    "All warnings": [
        "WARNING: obligatory col 'timestamp' has invalid format: 'timestamp'",
        "WARNING: obligatory col 'timestamp' has invalid format: 'timestamp'",
    ],
    "Number of events from all sources": {"SOURCE_1": 1},
    "Number of events from all levels": {"ERROR": 1},
    "TOP 5 sources by number of errors": ["SOURCE_1"],
}
