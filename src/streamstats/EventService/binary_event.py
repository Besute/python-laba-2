import json
import struct

from pathlib import Path

from streamstats.Errors.errors import ParserError
from streamstats.EventService.base_for_event import EventSkeleton


class BinaryEvent(EventSkeleton):
    MAGIC = b"BIN1"
    VERSION = 1
    HEADER_SIZE = 9

    def __init__(self, paths, skip_invalid=False):
        self.paths = paths
        self.skip_invalid = skip_invalid
        self._big_data = []
        super().__init__()

    @property
    def big_data(self):
        return self._big_data

    def read(self):
        result = []
        self._big_data = []
        for path in self.paths:
            path = Path(path)
            try:
                self._big_data.append(path.stat().st_size >= self.BIG_FILE_SIZE)
                with path.open("rb") as file:
                    data = file.read()
                result.append(self._parse(data))
            except (OSError, ValueError, struct.error) as e:
                if self.skip_invalid:
                    result.append(None)
                    continue
                raise ParserError(f"Failed to parse {path}: {e}") from e
        return result, self._big_data

    @staticmethod
    def _parse(data):
        view = memoryview(data)
        try:
            if len(view) < BinaryEvent.HEADER_SIZE:
                raise ValueError("Binary file is too small")

            if view[:4].tobytes() != BinaryEvent.MAGIC:
                raise ValueError("Invalid binary signature")
            version = view[4]
            if version != BinaryEvent.VERSION:
                raise ValueError(f"Unsupported binary version: {version}")
            payload_size = struct.unpack_from("<I", view, 5)[0]
            expected_size = BinaryEvent.HEADER_SIZE + payload_size
            if len(view) != expected_size:
                raise ValueError(
                    f"Invalid payload size: expected {payload_size} bytes, "
                    f"got {len(view) - BinaryEvent.HEADER_SIZE}"
                )
            payload = view[BinaryEvent.HEADER_SIZE : expected_size]
            text = payload.tobytes().decode("utf-8")
            records = []
            for line_number, line in enumerate(text.splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON on line {line_number}: {e}") from e
                if not isinstance(record, dict):
                    raise ValueError(f"JSON on line {line_number} must be an object")
                records.append(record)
            return records
        finally:
            view.release()
