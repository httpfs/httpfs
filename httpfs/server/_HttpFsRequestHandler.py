import base64
import http
import os
import stat

from ._JSONRequestHandler import _JSONRequestHandler
from httpfs.common import HttpFsRequest, HttpFsResponse
import logging
import errno


class _HttpFsRequestHandler(_JSONRequestHandler):
    STAT_FS_KEYS = [
        'f_bavail',
        'f_bfree',
        'f_blocks',
        'f_bsize',
        'f_favail',
        'f_ffree',
        'f_files',
        'f_flag',
        'f_frsize',
        'f_namemax'
    ]

    GETATTR_KEYS = [
        'st_atime',
        'st_ctime',
        'st_gid',
        'st_mode',
        'st_mtime',
        'st_nlink',
        'st_size',
        'st_uid'
    ]

    server_version = "HttpFs/0.1"
    sys_version = ""

    def log_message(self, format, *args):
        # Allow disable based on log level
        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            super().log_message(format, *args)

    def get_abs_path(self, client_path):
        client_path = client_path.lstrip("/")
        return os.path.join(self.server.get_fs_root(), client_path)

    def get_fs_lock(self):
        return self.server.get_fs_lock()

    def on_valid_request(self, request_dict):
        """
        Called when a valid JSON request has been sent from a client
        :param request_dict: JSON request converted to dict object
        """
        # TODO: API key authentication here
        try:
            if "User-Agent" not in self.headers or not self.headers["User-Agent"].startswith("HttpFsClient"):
                raise RuntimeError("Invalid User-Agent header: Client is not an HttpFsClient")

            request = HttpFsRequest.from_dict(request_dict)
            self._delegate_request(request)
        except ValueError as e:
            response = HttpFsResponse(errno.EIO, {"message": str(e)})
            self.send_json_response(http.HTTPStatus.BAD_REQUEST, response.as_dict())

    def _delegate_request(self, httpFsRequest):
        """
        Delegates the given request to the correct handler method
        :param httpfs_request_args: HttpFsRequest object
        """
        client = self.client_address[0]

        # TODO: Validate JSON arguments per request type

        if httpFsRequest.get_type() == HttpFsRequest.OP_ACCESS:
            logging.debug("Received access request from {}".format(client))
            return self.on_access(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_CREATE:
            logging.debug("Received create request from {}".format(client))
            return self.on_create(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_CHMOD:
            logging.debug("Received chmod request from {}".format(client))
            return self.on_chmod(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_CHOWN:
            logging.debug("Received chown request from {}".format(client))
            return self.on_chown(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_FLUSH:
            logging.debug("Received flush request from {}".format(client))
            return self.on_flush(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_FSYNC:
            logging.debug("Received fsync request from {}".format(client))
            return self.on_fsync(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_GET_ATTR:
            logging.debug("Received getattr request from {}".format(client))
            return self.on_getattr(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_LINK:
            logging.debug("Received link request from {}".format(client))
            return self.on_link(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_MKDIR:
            logging.debug("Received mkdir request from {}".format(client))
            return self.on_mkdir(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_MKNOD:
            logging.debug("Received mknod request from {}".format(client))
            return self.on_mknod(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_OPEN:
            logging.debug("Received open request from {}".format(client))
            return self.on_open(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_READ:
            logging.debug("Received read request from {}".format(client))
            return self.on_read(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_READDIR:
            logging.debug("Received readdir request from {}".format(client))
            return self.on_readdir(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_READLINK:
            logging.debug("Received readlink request from {}".format(client))
            return self.on_readlink(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_RELEASE:
            logging.debug("Received release request from {}".format(client))
            return self.on_release(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_RENAME:
            logging.debug("Received rename request from {}".format(client))
            return self.on_rename(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_RM_DIR:
            logging.debug("Received rmdir request from {}".format(client))
            return self.on_rmdir(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_STAT_FS:
            logging.debug("Received statfs request from {}".format(client))
            return self.on_statfs(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_SYMLINK:
            logging.debug("Received symlink request from {}".format(client))
            return self.on_symlink(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_TRUNCATE:
            logging.debug("Received truncate request from {}".format(client))
            return self.on_truncate(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_UNLINK:
            logging.debug("Received unlink request from {}".format(client))
            return self.on_unlink(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_UTIMENS:
            logging.debug("Received unlink request from {}".format(client))
            return self.on_utimens(httpFsRequest.get_args())

        elif httpFsRequest.get_type() == HttpFsRequest.OP_WRITE:
            logging.debug("Received write request from {}".format(client))
            return self.on_write(httpFsRequest.get_args())

        else:
            logging.warning("Recieved unknown request from {}".format(client))
            response_obj = HttpFsResponse(errno.EIO, {"message": "Method not implemented"})
            return self.send_json_response(
                http.HTTPStatus.BAD_REQUEST,
                response_obj.as_dict()
            )

    def on_invalid_request(self, err_msg):
        """
        Called when invalid JSON has been sent as a request from a client
        :param err_msg: The error message
        """
        logging.debug(
            "Invalid request received from {}: '{}'".format(
                self.client_address[0], err_msg
            )
        )
        response_obj = HttpFsResponse(
            errno.EIO,
            {"message": err_msg}
        )
        self.send_json_response(
            http.HTTPStatus.BAD_REQUEST,
            response_obj.as_dict()
        )

    def on_access(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_ACCESS is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        mode = httpfs_request_args["mode"]
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]
        file_stats = os.stat(path)

        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid
        read_requested = bool(mode & os.R_OK)
        write_requested = bool(mode & os.W_OK)
        execute_requested = bool(mode & os.X_OK)
        exists_requested = mode == os.F_OK

        access_ok = True

        # Exists requested
        if exists_requested:
            access_ok = os.path.exists(path)

        # Owner access
        if is_owner:
            owner_readable = bool(file_stats.st_mode & stat.S_IRUSR)
            owner_writeable = bool(file_stats.st_mode & stat.S_IWUSR)
            owner_executable = bool(file_stats.st_mode & stat.S_IXUSR)
            if read_requested:
                access_ok = access_ok and owner_readable
            if write_requested:
                access_ok = access_ok and owner_writeable
            if execute_requested:
                access_ok = access_ok and owner_executable
        # Group access
        elif is_group:
            group_readable = bool(file_stats.st_mode & stat.S_IRGRP)
            group_writeable = bool(file_stats.st_mode & stat.S_IWGRP)
            group_executable = bool(file_stats.st_mode & stat.S_IXGRP)
            if read_requested:
                access_ok = access_ok and group_readable
            if write_requested:
                access_ok = access_ok and group_writeable
            if execute_requested:
                access_ok = access_ok and group_executable
        # World access
        else:
            world_readable = bool(file_stats.st_mode & stat.S_IROTH)
            world_writeable = bool(file_stats.st_mode & stat.S_IWOTH)
            world_executable = bool(file_stats.st_mode & stat.S_IXGRP)
            if read_requested:
                access_ok = access_ok and world_readable
            if write_requested:
                access_ok = access_ok and world_writeable
            if execute_requested:
                access_ok = access_ok and world_executable

        if not access_ok:
            logging.warning("Error during access request: Access denied")
            response_obj.set_err_no(errno.EACCES)

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_create(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_ACCESS is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        dir_stats = os.stat(os.path.dirname(path))
        is_dir_owner = dir_stats.st_uid == uid
        is_dir_group = dir_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_dir_owner:
            access_ok = dir_stats.st_mode & stat.S_IWUSR
        elif is_dir_group:
            access_ok = dir_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = dir_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                fd = os.open(
                    path,
                    flags=os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_ASYNC | os.O_NOATIME,
                    mode=httpfs_request_args["mode"]
                )
                os.chown(path, uid, gid)
                response_obj.set_data({"file_descriptor": fd})
            else:
                logging.warning("Error during create request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})

        except Exception as e:
            logging.error("Error during create request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_chmod(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_FLUSH is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        client = self.client_address[0]
        path = self.get_abs_path(httpfs_request_args["path"])
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(path)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                os.chmod(
                    path,
                    httpfs_request_args["mode"]
                )
                logging.debug("Successful chmod for {}".format(client))
            else:
                logging.warning("Error during chmod request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})
        except Exception as e:
            logging.error("Error during chmod request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_chown(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_FLUSH is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        client = self.client_address[0]
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]
        caller_uid = httpfs_request_args["caller_uid"]
        caller_gid = httpfs_request_args["caller_gid"]

        file_stats = os.stat(path)
        is_owner = file_stats.st_uid == caller_uid
        is_group = file_stats.st_gid == caller_gid

        if caller_uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        # TODO: Don't let me if it isn't mine
        try:
            if access_ok:
                os.chown(path, uid, gid)
                logging.debug("Successful chown for {}".format(client))
            else:
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})
                logging.warning("Error during chown request: Access denied")
        except Exception as e:
            logging.error("Error during chown request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_flush(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_FLUSH is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()

        try:
            os.fsync(httpfs_request_args["file_descriptor"])
        except Exception as e:
            logging.error("Error during flush request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_fsync(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_FSYNC is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()

        try:
            if httpfs_request_args["datasync"]:
                os.fdatasync(httpfs_request_args["file_descriptor"])
            else:
                os.fsync(httpfs_request_args["file_descriptor"])
        except Exception as e:
            logging.error("Error during fsync request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_getattr(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_GET_ATTR is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])

        try:
            os_attrs = os.lstat(path)
            attrs = dict()

            for k in _HttpFsRequestHandler.GETATTR_KEYS:
                attrs[k] = getattr(os_attrs, k)

            response_obj.set_data(attrs)

        except FileNotFoundError:
            logging.warning("{} not found".format(path))
            response_obj.set_err_no(errno.ENOENT)

        self.send_json_response(200, response_obj.as_dict())

    def on_link(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_LINK is requested
        :param httpfs_request_args: The client request args dict
        """
        target_path = self.get_abs_path(httpfs_request_args["target"])
        source_path = self.get_abs_path(httpfs_request_args["source"])

        response_obj = HttpFsResponse()

        try:
            os.link(source_path, target_path)
        except Exception as e:
            logging.error("Error during link request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_mkdir(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_MKDIR is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])

        try:
            os.mkdir(path, mode=httpfs_request_args["mode"])
        except Exception as e:
            logging.error("Error during mkdir request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_mknod(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_MKNOD is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])

        try:
            os.mknod(path, mode=httpfs_request_args["mode"], device=httpfs_request_args["dev"])
        except Exception as e:
            logging.error("Error during mknod request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_open(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_OPEN is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])

        # Hardcode async and noatime
        flags = httpfs_request_args["flags"] | os.O_ASYNC | os.O_NOATIME

        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        dir_stats = os.stat(os.path.dirname(path))
        is_dir_owner = dir_stats.st_uid == uid
        is_dir_group = dir_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_dir_owner:
            access_ok = dir_stats.st_mode & stat.S_IXUSR
        elif is_dir_group:
            access_ok = dir_stats.st_mode & stat.S_IXGRP
        else:
            access_ok = dir_stats.st_mode & stat.S_IXOTH

        if access_ok and os.path.exists(path):
            file_stats = os.stat(path)
            is_owner = file_stats.st_uid == uid
            is_group = file_stats.st_gid == gid

            read_requested = (
                flags & os.O_RDONLY or
                flags & os.O_RDWR or
                flags & os.O_EXCL
            )
            write_requested = (
                flags & os.O_WRONLY or
                flags & os.O_RDWR or
                flags & os.O_APPEND
            )

            if uid == 0:
                access_ok = True
            elif is_owner:
                if read_requested:
                    access_ok = file_stats.st_mode & stat.S_IRUSR
                elif write_requested:
                    access_ok = file_stats.st_mode & stat.S_IWUSR
            elif is_group:
                if read_requested:
                    access_ok = file_stats.st_mode & stat.S_IRGRP
                elif write_requested:
                    access_ok = file_stats.st_mode & stat.S_IWGRP
            else:
                if read_requested:
                    access_ok = file_stats.st_mode & stat.S_IROTH
                elif write_requested:
                    access_ok = file_stats.st_mode & stat.S_IROTH

        try:
            if access_ok:
                fd = os.open(
                    self.get_abs_path(httpfs_request_args["path"]),
                    flags
                )
                response_obj.set_data({"file_descriptor": fd})
            else:
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})
                logging.warning("Error during open request: Access denied")

        except Exception as e:
            logging.error("Error during open request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_read(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_READ is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        file_descriptor = httpfs_request_args["file_descriptor"]
        offset = httpfs_request_args["offset"]
        size = httpfs_request_args["size"]

        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(file_descriptor)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IRUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IRGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IROTH

        try:
            if access_ok:
                with self.server.get_fs_lock():
                    os.lseek(file_descriptor, offset, os.SEEK_SET)
                    bytes_read = os.read(file_descriptor, size)
                response_obj.set_data({
                    "bytes_read": base64.standard_b64encode(bytes_read).decode("utf-8")
                })
            else:
                logging.warning("Error during read request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})

        except Exception as e:
            logging.error("Error during read request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_readdir(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_READDIR is requested
        :param httpfs_request_args: The client request args dict
        """
        path = self.get_abs_path(httpfs_request_args["path"])
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(path)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        response_obj = HttpFsResponse()

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IRUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IRGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IROTH

        if access_ok:
            dir_listing = os.listdir(path)
            dir_listing = [".", ".."] + dir_listing
            response_obj.set_data({"dir_listing": dir_listing})
        else:
            logging.warning("Error during readdir request: Access denied")
            response_obj.set_err_no(errno.EACCES)
            response_obj.set_data({"message": "Access denied"})

        self.send_json_response(200, response_obj.as_dict())

    def on_rename(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_RENAME is requested
        :param httpfs_request_args: The client request args dict
        """
        old_path = self.get_abs_path(httpfs_request_args["old_path"])
        new_path = self.get_abs_path(httpfs_request_args["new_path"])

        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(old_path)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        response_obj = HttpFsResponse()

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                os.rename(old_path, new_path)
            else:
                logging.warning("Error during rename request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})
        except Exception as e:
            logging.error("Error during rename request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_readlink(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_RELEASE is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        link_path = self.get_abs_path(httpfs_request_args["link_path"])

        try:
            target = os.readlink(link_path)
            if target.startswith("/"):
                target = os.path.relpath(target, self.server.get_fs_root())
                target = "/" + target
            response_obj.set_data({"target": target})
        except Exception as e:
            logging.error("Error during readlink request: {}".format(e))
            response_obj.set_err_no(errno.EIO)

        self.send_json_response(200, response_obj.as_dict())

    def on_release(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_RELEASE is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()

        try:
            os.close(httpfs_request_args["file_descriptor"])
        except Exception as e:
            logging.error("Error during release request: {}".format(e))
            response_obj.set_err_no(errno.EIO)

        self.send_json_response(200, response_obj.as_dict())

    def on_rmdir(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_RMDIR is requested
        :param httpfs_request_args: The client request args dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])

        try:
            os.rmdir(path)
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                logging.error("{} not found".format(path))
                err = errno.ENOENT
            elif isinstance(e, OSError):
                err = e.errno
            else:
                err = errno.EIO

            logging.error("Error during rmdir request: {}".format(e))
            response_obj.set_err_no(err)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(200, response_obj.as_dict())

    def on_statfs(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_STAT_FS is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        fs_path = self.get_abs_path(httpfs_request_args["path"])
        statfs_os_result = os.statvfs(fs_path)
        statfs_result = dict()

        for k in _HttpFsRequestHandler.STAT_FS_KEYS:
            statfs_result[k] = getattr(statfs_os_result, k)

        response_obj = HttpFsResponse(response_data=statfs_result)
        self.send_json_response(200, response_obj.as_dict())

    def on_symlink(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_SYMLINK is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        source = self.get_abs_path(httpfs_request_args["source"])
        target = self.get_abs_path(httpfs_request_args["target"])

        try:
            os.symlink(source, target)
        except Exception as e:
            logging.error("Error during symlink request: {}".format(e))
            response_obj.set_err_no(errno.EIO)

        self.send_json_response(200, response_obj.as_dict())

    def on_truncate(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_TRUNCATE is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        length = httpfs_request_args["length"]

        try:
            with open(path, 'r+') as f:
                f.truncate(length)
        except Exception as e:
            logging.error("Error during truncate request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(200, response_obj.as_dict())

    def on_unlink(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_UNLINK is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(path)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                os.unlink(path)
            else:
                logging.warning("Error during unlink request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})
        except Exception as e:
            logging.error("Error during unlink request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(200, response_obj.as_dict())

    def on_utimens(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_UTIMENS is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()
        path = self.get_abs_path(httpfs_request_args["path"])
        times = httpfs_request_args["times"]
        if isinstance(times, list):
            times = tuple(times)

        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(path)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                os.utime(path, times)
            else:
                logging.warning("Error during write request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})

        except Exception as e:
            logging.error("Error during utimens request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(http.HTTPStatus.OK, response_obj.as_dict())

    def on_write(self, httpfs_request_args):
        """
        Called when HttpFsRequest.OP_UTIMENS is received from the client
        :param httpfs_request_args: The client request arg dict
        """
        response_obj = HttpFsResponse()

        file_descriptor = httpfs_request_args["file_descriptor"]
        data = base64.standard_b64decode(httpfs_request_args["data"])
        offset = httpfs_request_args["offset"]

        uid = httpfs_request_args["uid"]
        gid = httpfs_request_args["gid"]

        file_stats = os.stat(file_descriptor)
        is_owner = file_stats.st_uid == uid
        is_group = file_stats.st_gid == gid

        if uid == 0:
            access_ok = True
        elif is_owner:
            access_ok = file_stats.st_mode & stat.S_IWUSR
        elif is_group:
            access_ok = file_stats.st_mode & stat.S_IWGRP
        else:
            access_ok = file_stats.st_mode & stat.S_IWOTH

        try:
            if access_ok:
                with self.server.get_fs_lock():
                    os.lseek(file_descriptor, offset, os.SEEK_SET)
                    bytes_written = os.write(file_descriptor, data)
                    logging.debug("{} wrote {} bytes".format(
                        self.client_address[0],
                        bytes_written)
                    )
                    response_obj.set_data({"bytes_written": bytes_written})
            else:
                logging.warning("Error during write request: Access denied")
                response_obj.set_err_no(errno.EACCES)
                response_obj.set_data({"message": "Access denied"})

        except Exception as e:
            logging.error("Error during write request: {}".format(e))
            response_obj.set_err_no(errno.EIO)
            response_obj.set_data({"message": str(e)})

        self.send_json_response(200, response_obj.as_dict())
