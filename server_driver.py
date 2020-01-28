import argparse
import logging

from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler


class _RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass


class Server(ThreadingHTTPServer):
    """
    Server that implements the _RequestHandler methods
    """

    # Otherwise python waits a really long time to release
    # the port after shutting down
    allow_reuse_address = True

    def __init__(self, port):
        super().__init__(("", port), _RequestHandler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="Port to run the server on", type=int)
    args = vars(parser.parse_args())

    logging.basicConfig(level=logging.DEBUG)
    server = Server(args["port"])

    try:
        print("Server running on port {}...".format(args["port"]))
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


