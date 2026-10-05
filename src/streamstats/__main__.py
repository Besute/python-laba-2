import argparse
from streamstats.Server.server import Server
from streamstats.parsers import BasicJsonParser

class PostJson(BasicJsonParser):
    def __init__(self, filename, format_, output, skip_invalid):
        dct = {
            "filename": filename,
            "format": format_,
            "output": output,
            "skipInvalid": skip_invalid
        }
        self.curr_json = self.parse_to_json(dct)

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

def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.command == "analyze":
            post_request = PostJson(args.FILE, args.format, args.output, args.skip_invalid)
            server = Server(post_request)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()