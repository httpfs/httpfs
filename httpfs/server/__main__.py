import argparse
import logging
import sys

from httpfs.server import HttpFsServer

LOG_FMT = "[%(asctime)s][%(levelname)s] %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"

parser = argparse.ArgumentParser(prog="httpfs.server")
parser.add_argument("port", help="Port to run the server on", type=int)
parser.add_argument(
    "fs_root",
    help="The directory to serve as a network filesystem"
)
parser.add_argument(
    "--tls-key",
    dest="tls_key",
    help="HTTPS server key",
    default=None
)
parser.add_argument(
    "--tls-cert",
    dest="tls_cert",
    help="HTTPS server cert",
    default=None
)
parser.add_argument(
    "--cred-store",
    dest="cred_store",
    help="JSON file with list of API keys",
    default=None
)
parser.add_argument(
    "--verbose",
    help="Be verbose",
    action="store_true"
)
args = parser.parse_args()

log_level = logging.WARN
if args.verbose:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level, format=LOG_FMT, datefmt=DATE_FMT)

try:
    server = HttpFsServer(
        args.port,
        args.fs_root,
        cred_store_file=args.cred_store,
        tls_key=args.tls_key,
        tls_cert=args.tls_cert
    )
except Exception as e:
    logging.error(e)
    sys.exit(1)

try:
    print("Server running on port {}...".format(args.port))
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
except Exception as e:
    logging.error(e)
    server.shutdown()
