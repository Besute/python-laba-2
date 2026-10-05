import json

class BasicJsonParser:

    @classmethod
    def parse_to_string(cls, data):
        return json.loads(data)

    @classmethod
    def parse_to_json(cls, data):
        return json.dumps(data)