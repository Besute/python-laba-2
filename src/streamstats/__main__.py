import argparse
import asyncio

from streamstats.Parsers.json_parser import BasicJsonParser
from streamstats.Server.server import Server

from .Errors.errors import StreamStatsError


class PostJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "POST"

    def __str__(self):
        return f"{self.method, self.curr_json}"


class GetJson(BasicJsonParser):
    def __init__(self, data):
        self.curr_json = self.to_json(data)
        self.method = "GET"

    def __str__(self):
        return f"{self.method, self.curr_json}"


def create_parser():
    parser = argparse.ArgumentParser(prog="streamstats", description="Analyze the csv and jsonl file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("FILE", type=str, nargs="+", help="files to analyze")
    analyze_parser.add_argument(
        "--format", type=str, required=True, choices=["csv", "jsonl"], help="format of input files"
    )
    analyze_parser.add_argument("--output", type=str, default="output/REPORT.json", help="output file")
    analyze_parser.add_argument("--skip-invalid", action="store_true", help="skip invalid rows")
    # analyze_parser.add_argument("--add-to-prev-data", action="store_true", help="add new data to previous data", default=False)

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
                    "skipInvalid": args.skip_invalid,
                }
            )
            server = Server(args.output)
            analyzed_data = await server.make_request(get_request)
            post_request = PostJson({"data": analyzed_data})
            await server.make_request(post_request)
    except Exception as err:
        raise StreamStatsError(f"Something went wrong: {err}")

    return 0


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
