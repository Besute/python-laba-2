JSONL_RES = [
    [
        {"timestamp": "2026-10-11T14:30:00Z", "level": "DEBUGG", "source": " 123", "message": "Hello", "C6": "RRRRR"},
        {"timestamp": "2026-10-11T14:30:00Z", "level": "DEBUG", "source": " 123", "message": "Hello", "C6": "RRRRR"},
    ]
]

CSV_RES = [
    [
        {"timestamp": "timestamp", "level": "C2", "source": "C3", "message": "C4"},
        {"timestamp": "timestamp", "level": "level", "source": "source", "message": "message"},
        {"timestamp": "2023-10-11T14:30:00Z", "level": "ERROR", "source": "SOURCE_1", "message": "Four"},
    ]
]

REPORT_JSONL = {
    "Total events": 2,
    "Minimum time": "2026-10-11T14:30:00+00:00",
    "Maximum time": "2026-10-11T14:30:00+00:00",
    "All warnings": ["WARNING: obligatory col 'level' has invalid format: 'DEBUGG'"],
    "Number of events from all sources": {" 123": 1},
    "Number of events from all levels": {"DEBUG": 1},
    "TOP 5 sources by number of errors": [],
}

REPORT_CSV = {
    "Total events": 3,
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
