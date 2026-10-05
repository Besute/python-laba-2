import argparse
import asyncio
from streamstats.Server.server import Server
from streamstats.parsers import BasicJsonParser

class PostJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "POST"

class GetJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "GET"

def create_parser():
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description="Analyze the csv and jsonl file"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("FILE", type=str)
    analyze_parser.add_argument("--format", type=str, required=True)
    analyze_parser.add_argument("--output", type=str, default="OUTPUT.csv")
    analyze_parser.add_argument("--skip-invalid", action="store_true")

    return parser

async def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.command == "analyze":
            post_request = PostJson(
        {
            "path": args.FILE,
            "type": args.format,
            "output": args.output,
            "skipInvalid": args.skip_invalid,
        }
            )
            print(post_request.__dict__)
            server = Server()
            print("SERVER CREATED")
            await server.make_request(post_request)
            print(server.__dict__)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())