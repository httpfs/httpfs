# pylint: disable=unused-argument

"""
Contains a class to be passed to fusepy.FUSE to handle filesystem operations
"""

import base64
import binascii
import errno
import logging
import os
import time

import requests
from fuse import Operations, FuseOSError, fuse_get_context

from httpfs.common import HttpFsRequest, HttpFsResponse
from .fuse_logger import _FuseLogger


class HttpFsClient(_FuseLogger, Operations):
    """
    A FUSE client that talks to an HttpFs server
    """

    client_version = 0.1
    _ONE_KILOBYTE = 1024

    def __init__(self, hostname, port, api_key=None, ca_file=None):
        """
        Constructor
        :param server: The server to connect to
        :param ca_file: Optional CA cert file if the server uses HTTPS
        """
        # Now we can use ipv6 addr
        self.server_hostname = hostname
        self._server_url = "http"
        if ca_file is not None and os.path.exists(ca_file):
            os.environ["REQUESTS_CA_BUNDLE"] = ca_file
            self._server_url += "s"
        self._server_url += "://{}:{}".format(hostname, port)
        self._http_keepalive_session = requests.Session()
        self._http_keepalive_session.headers.update({
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": "HttpFsClient/{}".format(HttpFsClient.client_version),
            "Host": self.server_hostname
        })
        self._api_key = api_key

    # Unimplemented filesystem ops
    bmap = None
    getxattr = None
    listxattr = None

    def _send_request(self, request_type, **kwargs):
        """
        Sends an HttpFsRequest of the given type with the given kwargs
        :param request_type: The request type to send
        :param kwargs: The arguments for the request
        :return: The HttpFsResponse
        """
        request = HttpFsRequest(
            request_type,
            kwargs
        )

        try:
            headers = dict()
            if self._api_key is not None:
                headers["Authorization"] = self._api_key

            response = self._http_keepalive_session.post(
                self._server_url,
                json=request.as_dict(),
                allow_redirects=False,
                timeout=10,
                headers=headers,
                stream=True
            )

            response.raise_for_status()

            # Minimal server response validation
            is_json = response.headers.get("Content-Type").startswith(
                "application/json"
            )
            is_httpfs_server = response.headers.get("Server").startswith(
                "HttpFs"
            )
            if not is_json or not is_httpfs_server:
                logging.error("Server response didn't come from HttpFs")
                raise FuseOSError(errno.EIO)

            return HttpFsResponse.from_dict(response.json())

        except requests.exceptions.HTTPError as http_error:
            logging.error(http_error)
            raise FuseOSError(errno.EACCES)
        except Exception as exception:
            logging.error(exception)
            raise FuseOSError(errno.EIO)

    def access(self, path, mode):
        """
        Check file access permissions
        :param path: Path to file to check
        :param mode: Mode to test
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_ACCESS,
            path=path,
            mode=mode,
            uid=uid,
            gid=gid
        )
        if response_obj.is_error():
            raise FuseOSError(errno.EACCES)

    def create(self, path, mode, fh=None):
        """
        Create and open a file
        If the file does not exist, first create it with the specified mode,
        and then open it.
        :param path: Path to file
        :param mode: Mode to create the file with
        :param fh: Optional file handle for the file we're creating
        :return: If fh=None, return file handle for the new file; Otherwise
        use fh to create the new file and return zero on success
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_CREATE,
            path=path,
            mode=mode,
            uid=uid,
            gid=gid
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

        return response_obj.get_data()["file_descriptor"]

    def chmod(self, path, mode):
        """
        Change permissions on path to mode
        :param path: Path to file/directory
        :param mode: New permissions
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_CHMOD,
            path=path,
            mode=mode,
            uid=uid,
            gid=gid
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def chown(self, path, uid, gid):
        """
        Change ownership on path to uid and gid
        :param path: Path to file/directory
        :param uid: New user id
        :param gid: New group id
        """
        caller_uid, caller_gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_CHOWN,
            path=path,
            uid=uid,
            gid=gid,
            caller_uid=caller_uid,
            caller_gid=caller_gid
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def flush(self, path, fh=None):
        """
        Possibly flush cached data.
        Flush is called on each close() of a file descriptor, as opposed
        to release() which is called on the close of the last file descriptor
        for a file
        :param path: Path to file
        :param fh: Optional file handle for the file to flush
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_FLUSH,
            file_descriptor=fh
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def fsync(self, path, datasync=False, fh=None):
        """
        Synchronize file contents
        If the datasync parameter is True, then only the user data should
        be flushed, not the meta data.
        :param path: Path to file file to sync
        :param datasync: Whether to sync data only an skip metadata
        :param fh: Optional file handle for the file to sync
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_FSYNC,
            file_descriptor=fh,
            datasync=datasync
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def getattr(self, path, fh=None):
        """
        Similar to stat(), retrieve file attributes
        :param path: path to the file
        :param fh: None if the current file isn't open
        :return:
        """
        response_obj = self._send_request(HttpFsRequest.OP_GET_ATTR, path=path)
        if response_obj.get_error_no() == 0:
            return response_obj.get_data()

        raise FuseOSError(response_obj.get_error_no())

    def link(self, target, source):
        """
        Create a hard link pointing to source named target
        :param target: Original file
        :param source: Link name
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_LINK, target=target, source=source)
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def mkdir(self, path, mode):
        """
        Create a new directory
        :param path: Path to new directory
        :param mode: Permissions for the new directory
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_MKDIR, path=path, mode=mode)
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def mknod(self, path, mode, dev):
        """
        Create a file node
        This is called for creation of all non-directory, non-symlink nodes. If
        the filesystem defines a create() method, then for regular files that
        will be called instead.
        :param path: Path to new node (file)
        :param mode: Permissions for new node
        :param dev: Whether node is a 'special file' (i/o device)
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_MKNOD, path=path, mode=mode, dev=dev)
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def open(self, path, flags):
        """
        Opens a file
        :param path: Path to file to open
        :param flags: See https://docs.python.org/3/library/functions.html#open
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_OPEN,
            path=path,
            flags=flags,
            uid=uid,
            gid=gid
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

        return response_obj.get_data()["file_descriptor"]

    def read(self, path, size, offset, fh=None):
        """
        Read at most size bytes from the file at path or fh. Start reading
        at offset
        :param path: Path to file
        :param size: Number of bytes to read
        :param offset: Offset from byte 0 at which to start reading
        :param fh: Optional file handle
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_READ,
            file_descriptor=fh,
            size=size,
            offset=offset,
            uid=uid,
            gid=gid
        )

        if response_obj.is_error():
            logging.error(
                "Read failed for %s: '%s'",
                response_obj.get_data()["message"],
                path
            )
            raise FuseOSError(response_obj.get_error_no())

        try:
            return base64.standard_b64decode(response_obj.get_data()["bytes_read"])
        except binascii.Error as encoding_error:
            logging.error("Error decoding read data: '%s'", encoding_error)
            raise FuseOSError(errno.EIO)

    def readdir(self, path, fh=None):
        """
        Return the directory listing at path
        :param path: Path to directory to list
        :param fh: Optional file handle for the directory
        :return: List of directory entries
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_READDIR,
            path=path,
            uid=uid,
            gid=gid
        )
        if response_obj.get_error_no() == 0:
            return response_obj.get_data()["dir_listing"]

        raise FuseOSError(response_obj.get_error_no())

    def readlink(self, link):
        """
        Return a string representing the path to which the symbolic link points.
        :param link: Path to link
        :return: Path to file that link points at
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_READLINK, link_path=link)
        if response_obj.get_error_no() == 0:
            return response_obj.get_data()["target"]

        raise FuseOSError(response_obj.get_error_no())

    def release(self, path, fh=None):
        """
        Release path's write lock
        :param path: Path to file
        :param fh: Optional file handle
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_RELEASE, file_descriptor=fh)
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def rename(self, old, new):
        """
        Move file at path old to path new
        :param old: Path to 'old' file
        :param new: Path to 'new' file
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_RENAME,
            old_path=old,
            new_path=new,
            uid=uid,
            gid=gid
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def rmdir(self, path, *args, dir_fh=None):
        """
        Removes the directory at path
        :param path: Path to directory to move
        :param args: Optional remove args
        :param dir_fh: Optional file handle for the directory
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_RM_DIR,
            path=path
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def statfs(self, path):
        """
        Get file system statistics for the filesystem at path
        :param path: Path to the filesystem
        :return:
        """
        response_obj = self._send_request(HttpFsRequest.OP_STAT_FS, path=path)

        if response_obj.get_error_no() == 0:
            return response_obj.get_data()

        raise FuseOSError(response_obj.get_error_no())

    def symlink(self, target, source):
        """
        Create a symlink that points to target and is named source
        :param target: Real file
        :param source: New symlink
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_SYMLINK,
            target=target,
            source=source
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def truncate(self, path, length, fh=None):
        """
        Resize path to length length
        :param path: Path to file to truncate
        :param length: New length of file
        :param fh: Optional file handle
        :return:
        """
        response_obj = self._send_request(
            HttpFsRequest.OP_TRUNCATE,
            path=path,
            length=length
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def unlink(self, path, *args, dir_fh=None):
        """
        Remove (delete) the file path.
        :param path: Path to file to delete
        :param args: Optional args
        :param dir_fh: Optional directory file handle
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_UNLINK,
            path=path,
            uid=uid,
            gid=gid
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def utimens(self, path, times=None):
        """
        Set the access and modified times of the file specified by path.
        If ns is specified, it must be a 2-tuple of the form
            (atime_ns, mtime_ns) where each member is an int expressing
            nanoseconds.
        If times is not None, it must be a 2-tuple of the form (atime, mtime)
            where each member is an int or float expressing seconds.
        If times is None and ns is unspecified, this is equivalent to
            specifying ns=(atime_ns, mtime_ns) where both times are the
            current time.
        :param path: Path to file to update
        :param times: Time tuple
        :return:
        """
        uid, gid, _ = fuse_get_context()
        response_obj = self._send_request(
            HttpFsRequest.OP_UTIMENS,
            path=path,
            times=times,
            uid=uid,
            gid=gid
        )
        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            raise FuseOSError(response_obj.get_error_no())

    def write(self, path, data, offset, fh=None):
        """
        Write data to path at offset
        :param path: Path to file to write to
        :param data: Data (bytes) to write
        :param offset: Byte at which to start writing
        :param fh: Optional file handle
        :return: The number of bytes actually written
        """
        start_time = time.time()
        uid, gid, _ = fuse_get_context()

        response_obj = self._send_request(
            HttpFsRequest.OP_WRITE,
            file_descriptor=fh,
            data=base64.standard_b64encode(data).decode("utf-8"),
            offset=offset,
            uid=uid,
            gid=gid
        )

        if response_obj.is_error():
            logging.error(response_obj.get_data()["message"])
            return FuseOSError(response_obj.get_error_no())

        bytes_written = response_obj.get_data()["bytes_written"]
        elapsed_time = time.time() - start_time

        # Print 1/10 of the time
        logging.debug(
            "Took {:.2f}s to write {} bytes ({:.2f} MB/s)".format(
                elapsed_time,
                bytes_written,
                bytes_written / 1024**2 / elapsed_time
            )
        )

        return bytes_written
