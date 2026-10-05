from pathlib import Path

class EventService:
    _path = ""
    _type = ""
    _output = ""

    def __init__(self, path, type_, output):
        self._path = path
        self._type = type_
        self._output = output
