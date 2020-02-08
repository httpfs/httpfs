#!/usr/bin/env python3
import argparse
import logging
import os
import requests

from fuse import FUSE, Operations, LoggingMixIn


class HttpFsClient(LoggingMixIn, Operations):
    def __init__(self, server):
        self._server = "http://{}".format(server)

    # Unimplemented filesystem ops
    bmap = None
    getxattr = None
    listxattr = None

    def init(self, path):
        super()
        try:
            response = requests.head(self._server)
            if response.status_code >= 200:
                logging.info("Server at {} responded".format(self._server))
            else:
                logging.warning("Server at {} returned {}".format(
                    self._server,
                    response.status_code
                ))
        except requests.exceptions.ConnectionError:
            logging.warning(
                "Server at {} is not responding".format(self._server)
            )

    def access(self, path, mode):
        """
        Check file access permissions
        :param path: Path to file to check
        :param mode: Mode to test
        :return:
        """
        pass

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
        pass

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
        pass

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
        pass

    def getattr(self, path, fh=None):
        """
        Similar to stat(), retrieve file attributes
        :param path: path to the file
        :param fh: None if the current file isn't open
        :return:
        """
        attrs = {
            'st_atime': 0,
            'st_ctime': 0,
            'st_gid': 0,
            'st_mode': 0,
            'st_mtime': 0,
            'st_nlink': 0,
            'st_size': 0,
            'st_uid': 0
        }
        return attrs

    def link(self, target, source):
        """
        Create a hard link from source pointing to target
        :param target: Original file
        :param source: Link name
        :return:
        """
        pass

    def mkdir(self, path, mode):
        """
        Create a new directory
        :param path: Path to new directory
        :param mode: Permissions for the new directory
        :return:
        """
        pass

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
        pass

    def open(self, path, flags):
        """
        Opens a file
        :param path: Path to file to open
        :param flags: See https://docs.python.org/3/library/functions.html#open
        :return:
        """
        pass

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
        pass

    def readdir(self, path, fh=None):
        """
        Return the directory listing at path
        :param path: Path to directory to list
        :param fh: Optional file handle for the directory
        :return: List of directory entries
        """
        pass

    def readlink(self, link):
        """
        Return a string representing the path to which the symbolic link points.
        :param link: Path to link
        :return: Path to file that link points at
        """
        pass

    def release(self, path, fh=None):
        """
        Release path's write lock
        :param path: Path to file
        :param fh: Optional file handle
        :return:
        """
        pass

    def rename(self, old, new):
        """
        Move file at path old to path new
        :param old: Path to 'old' file
        :param new: Path to 'new' file
        :return:
        """
        pass

    def rmdir(self, path, *args, dir_fh=None):
        """
        Removes the directory at path
        :param path: Path to directory to move
        :param args: Optional remove args
        :param dir_fh: Optional file handle for the directory
        :return:
        """
        pass

    def statfs(self, path):
        """
        Get file system statistics for the filesystem at path
        :param path: Path to the filesystem
        :return:
        """
        fs_stats = {
            'f_bavail': -1,
            'f_bfree': -1,
            'f_blocks': -1,
            'f_bsize': -1,
            'f_favail': -1,
            'f_ffree': -1,
            'f_files': -1,
            'f_flag': -1,
            'f_frsize': -1,
            'f_namemax': -1
        }
        return fs_stats

    def symlink(self, target, source):
        """
        Create a symlink that points to target and is named source
        :param target: Real file
        :param source: New symlink
        :return:
        """
        pass

    def truncate(self, path, length, fh=None):
        """
        Resize path to length length
        :param path: Path to file to truncate
        :param length: New length of file
        :param fh: Optional file handle
        :return:
        """
        pass

    def unlink(self, path, *args, dir_fh=None):
        """
        Remove (delete) the file path.
        :param path: Path to file to delete
        :param args: Optional args
        :param dir_fh: Optional directory file handle
        :return:
        """
        pass

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
        pass

    def write(self, path, data, offset, fh=None):
        """
        Write data to path at offset
        :param path: Path to file to write to
        :param data: Data (bytes) to write
        :param offset: Byte at which to start writing
        :param fh: Optional file handle
        :return:
        """
        pass


# TODO: Move to separate file
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "server",
        help="The hostname an port of the server to connect to"
    )
    parser.add_argument(
        'mount',
        help="The client directory to mount the server filesystem onto"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    try:
        # Create the mount directory
        if not os.path.exists(args.mount):
            os.mkdir(args.mount)

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
