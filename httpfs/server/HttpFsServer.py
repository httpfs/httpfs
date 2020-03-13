import logging
import os
import threading
from http.server import ThreadingHTTPServer
from ._HttpFsRequestHandler import _HttpFsRequestHandler


class HttpFsServer(ThreadingHTTPServer):
    """
    Server that implements the HttpFsRequestHandler methods
    """

    # Otherwise python waits a really long time to release
    # the port after shutting down
    allow_reuse_address = True

    def __init__(self, port, fs_root):
        self._fs_root = os.path.realpath(fs_root)
        self._fs_lock = threading.Lock()

        if not os.path.exists(self._fs_root):
            raise RuntimeError(
                "Filesystem root '{}' doesn't exist".format(self._fs_root)
            )

        super().__init__(("", port), _HttpFsRequestHandler)

    def get_fs_root(self):
        return self._fs_root

    def get_fs_lock(self):
        return self._fs_lock
