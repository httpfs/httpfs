"""
Main method for running the HttpFs client via fusepy
"""

import argparse
import logging
import os
import sys

from fuse import FUSE
from httpfs.client import HttpFsClient

LOG_FMT = "[%(asctime)s][%(levelname)s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

PARSER = argparse.ArgumentParser(prog="httpfs.client")
PARSER.add_argument(
    "server",
    help="The hostname an port of the server to connect to"
)
PARSER.add_argument(
    'mount',
    help="The client directory to mount the server filesystem onto"
)
PARSER.add_argument(
    "--ca-file",
    dest="ca_file",
    help="CA certificate file if the server uses HTTPS",
    default=None
)
PARSER.add_argument(
    "--api-key",
    dest="api_key",
    help="API key if the server uses authentication",
    default=None
)
PARSER.add_argument(
    "--verbose",
    dest="verbose",
    help="Be verbose",
    action="store_true"
)
ARGS = PARSER.parse_args()

log_level = logging.WARN
if ARGS.verbose:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level, format=LOG_FMT, datefmt=DATE_FMT)

try:
    # Create the mount directory
    if not os.path.exists(ARGS.mount):
        logging.error("Mount point '%s' does not exist", ARGS.mount)
        sys.exit(1)

    [HOSTNAME, PORT] = ARGS.server.rsplit(':', 1)

    # Mount the filesystem
    FUSE(
        HttpFsClient(HOSTNAME, PORT, api_key=ARGS.api_key, ca_file=ARGS.ca_file),
        ARGS.mount,
        foreground=True,
        allow_other=True
    )
except Exception as exception:
    logging.error("ERROR: %s", exception)
