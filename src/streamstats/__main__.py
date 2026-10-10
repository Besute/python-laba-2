import argparse
import asyncio

from streamstats.Parsers.parsers import BasicJsonParser
from streamstats.Server.server import Server


class PostJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "POST"


class GetJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "GET"


def create_parser():
    parser = argparse.ArgumentParser(prog="streamstats", description="Analyze the csv and jsonl file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("FILE", type=str, nargs="+", help="files to analyze")
    analyze_parser.add_argument(
        "--format", type=str, required=True, choices=["csv", "jsonl"], help="format of input files"
    )
    analyze_parser.add_argument("--output", type=str, default="OUTPUT.csv", help="output file")
    analyze_parser.add_argument("--skip-invalid", action="store_true", help="skip invalid rows")

    return parser


async def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.command == "analyze":
            get_request = GetJson(
                {
                    "path": args.FILE,
                    "type": args.format,
                    "output": args.output,
                    "skipInvalid": args.skip_invalid,
                }
            )
            print("Connecting...")
            server = Server()
            print("Connected!")
            analyzed_data = await server.make_request(get_request)
            print(analyzed_data)
            post_request = PostJson({"data": analyzed_data})
            await server.make_request(post_request)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
