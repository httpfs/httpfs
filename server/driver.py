#!/usr/bin/env python3

import argparse
import json
import logging

from http.server import ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler


class _RequestHandler(SimpleHTTPRequestHandler):
    @staticmethod
    def _dict_to_bytes(dict_obj):
        return json.dumps(dict_obj).encode("utf-8")

    def do_GET(self):
        self.send_response(500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(_RequestHandler._dict_to_bytes({
            "message": "Not implemented yet"
        }))

    def do_POST(self):
        self.send_response(500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(_RequestHandler._dict_to_bytes({
            "message": "Not implemented yet"
        }))

    def do_PUT(self):
        self.send_response(500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(_RequestHandler._dict_to_bytes({
            "message": "Not implemented yet"
        }))

    def do_DELETE(self):
        self.send_response(500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(_RequestHandler._dict_to_bytes({
            "message": "Not implemented yet"
        }))


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


