import argparse
import logging
import sys

from httpfs.server import HttpFsServer

LOG_FMT = "[%(asctime)s][%(levelname)s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=logging.DEBUG, format=LOG_FMT, datefmt=DATE_FMT)
parser = argparse.ArgumentParser(prog="httpfs.server")
parser.add_argument("port", help="Port to run the server on", type=int)
parser.add_argument("fs_root", help="The directory to serve as a network filesystem")
args = parser.parse_args()

try:
    server = HttpFsServer(args.port, args.fs_root)
except RuntimeError as e:
    logging.error(e)
    sys.exit(1)

try:
    print("Server running on port {}...".format(args.port))
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
