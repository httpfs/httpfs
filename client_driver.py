#!/usr/bin/env python3
import argparse
import logging

from fuse import FUSE, Operations, LoggingMixIn


class HttpFsClient(LoggingMixIn, Operations):
    def __init__(self, root):
        pass

    # Skip extended file attribs
    getxattr = None
    listxattr = None

    def access(self, path, mode):
        pass

    def create(self, path, mode, fi=None):
        pass

    def flush(self, path, fh):
        pass

    def fsync(self, path, datasync, fh):
        pass

    def getattr(self, path, fh=None):
        pass

    def link(self, target, source):
        pass

    def mkdir(self, path, mode):
        pass

    def mknod(self, path, mode, dev):
        pass

    def open(self, path, flags):
        pass

    def read(self, path, size, offset, fh):
        pass

    def readdir(self, path, fh):
        pass

    def readlink(self, link):
        pass

    def release(self, path, fh):
        pass

    def rename(self, old, new):
        pass

    def rmdir(self, path, *args, dir_fd=None):
        pass

    def statfs(self, path):
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
        pass

    def truncate(self, path, length, fh=None):
        pass

    def unlink(self, path, *args, dir_fd=None):
        pass

    def utimens(self, path, times=None):
        pass

    def write(self, path, data, offset, fh):
        pass


# TODO: Move to separate file
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help="The directory to mount as the 'server")
    parser.add_argument('mount', help="The client directory to mount the 'server' filesystem onto")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(HttpFsClient(args.root), args.mount, foreground=True, allow_other=True)
