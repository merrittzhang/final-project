from argparse import ArgumentParser

import sys

import server


DB_URL = ""


def handle_args():
    """
    Handle and return arguments using ArgumentParser.
    """
    parser = ArgumentParser(prog=sys.argv[0],
                            description="SQLite3 Web Browser",
                            allow_abbrev=False)
    parser.add_argument("file", type=str,
                        help="the database file to connect to")
    parser.add_argument("port", type=int,
                        help="the port at which the server should listen")
    return vars(parser.parse_args())['file'], vars(parser.parse_args())['port']


def main():
    file, port = handle_args()
    server.DB_URL = file

    try:
        server.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(sys.argv[0] + ": " + str(ex), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()