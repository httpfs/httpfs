import argparse
import logging
import os
import sys

from fuse import FUSE
from httpfs.client import HttpFsClient

LOG_FMT = "[%(asctime)s][%(levelname)s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

# TODO: Allow configure log verbosity
logging.basicConfig(level=logging.DEBUG, format=LOG_FMT, datefmt=DATE_FMT)
parser = argparse.ArgumentParser(prog="httpfs.client")
parser.add_argument(
    "server",
    help="The hostname an port of the server to connect to"
)
parser.add_argument(
    'mount',
    help="The client directory to mount the server filesystem onto"
)
args = parser.parse_args()

try:
    # Create the mount directory
    if not os.path.exists(args.mount):
        logging.error("Mount point '{}' does not exist".format(args.mount))
        sys.exit(1)

    # Mount the filesystem
    FUSE(
        HttpFsClient(args.server),
        args.mount,
        foreground=True,
        allow_other=True
    )
except RuntimeError as e:
    logging.error("ERROR: {}".format(e))
except PermissionError as e:
    logging.error("ERROR: {}".format(e))
