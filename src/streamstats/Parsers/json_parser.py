import json


class BasicJsonParser:
    @classmethod
    def to_json(cls, data):
        return json.dumps(data)

    @classmethod
    def from_json(cls, data):
        return json.loads(data)
