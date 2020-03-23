import os
import socket
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

    # TCP keepAlive activates after 1 second of idle connection,
    # sends a ping every 3 seconds, and closes after 1 failed ping
    _tcp_keepidle_secs = 1
    _tcp_keep_interval_secs = 3
    _tcp_keep_max_fails = 1

    def __init__(self, port, fs_root):
        super().__init__(("", port), _HttpFsRequestHandler)

        self._fs_root = os.path.realpath(fs_root)
        self._fs_lock = threading.Lock()

        # This line fixes the HTTP/1.1 keep-alive delay
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # These options configure TCP keep-alive, which is different
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPIDLE,
            HttpFsServer._tcp_keepidle_secs
        )
        self.socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPINTVL,
            HttpFsServer._tcp_keep_interval_secs
        )
        self.socket.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPCNT,
            HttpFsServer._tcp_keep_max_fails
        )

        if not os.path.exists(self._fs_root):
            raise RuntimeError(
                "Filesystem root '{}' doesn't exist".format(self._fs_root)
            )

    def get_fs_root(self):
        return self._fs_root

    def get_fs_lock(self):
        return self._fs_lock
