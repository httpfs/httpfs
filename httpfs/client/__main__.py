import argparse
import logging
import os
import sys
import yaml
from httpfs.common._CredModels import _Cred, _CredStore
from httpfs.common._CredStorage import _TextCredStore

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
    if not os.path.exists('./config.yaml'):
        logging.error("Config file './config.yaml' does not exist")
        with open('./config.yaml', 'w') as file:
            file.write('# Config Example:\n' +
                       '# User: My Name\n' + '# CredFile: ./creds\n')
        exit(1)
    config = None
    with open('./config.yaml', 'r') as file:
        config = yaml.load(file, yaml.Loader)
    credStore = _TextCredStore(config['CredFile'])
    [hostname, port] = args.server.rsplit(':', 1)
    cred = credStore.getCred(hostname, config['User'])
    if cred is None:
        logging.error("You have no API key for '{}'".format(hostname))
        exit(1)
    # Mount the filesystem
    FUSE(
        HttpFsClient(hostname, port, cred),
        args.mount,
        foreground=True,
        allow_other=True
    )
except RuntimeError as e:
    logging.error("ERROR: {}".format(e))
except PermissionError as e:
    logging.error("ERROR: {}".format(e))
