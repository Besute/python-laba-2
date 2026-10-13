import json

event = {"timestamp": "2026-10-11T14:30:00Z", "level": "ddd", "source": " 123", "message": "Hello", "C5": "There!"}


def generate_big_data(iters):
    """
    This function generates big jsonl file. Approx. weight with iters=10_000_000 >= 1GB
    """
    with open("data/large.jsonl", "w", encoding="utf-8") as f:
        for i in range(iters):
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
