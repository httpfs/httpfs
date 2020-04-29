class HttpFsRequest:
    """
    Class representing a filesystem operation with JSON
    serialization/deserialization methods
    """
    OP_ACCESS = 0
    OP_CREATE = 1
    OP_FLUSH = 2
    OP_FSYNC = 3
    OP_GET_ATTR = 4
    OP_LINK = 5
    OP_MKDIR = 6
    OP_MKNOD = 7
    OP_OPEN = 8
    OP_READ = 9
    OP_READDIR = 10
    OP_READLINK = 11
    OP_RELEASE = 12
    OP_RENAME = 13
    OP_RM_DIR = 14
    OP_STAT_FS = 15
    OP_SYMLINK = 16
    OP_TRUNCATE = 17
    OP_UNLINK = 18
    OP_UTIMENS = 19
    OP_WRITE = 20
    OP_CHOWN = 21
    OP_CHMOD = 22

    def __init__(self, op_type, args_dict, api_key=None):
        """
        Class cooresponding to the schema
        https://raw.githubusercontent.com/httpfs/httpfs/master/HttpFsRequest.schema.json
        :param op_type: One of the operation types above
        :param args_dict: Arguments for the operation
        :param api_key: API key for authentication with the server
        """
        self._type = op_type
        self._args = args_dict
        self._api_key = api_key

    def get_type(self):
        return self._type

    def get_args(self):
        return self._args

    @staticmethod
    def from_dict(json_dict):
        try:
            for k in ["type", "args"]:
                if k not in json_dict.keys():
                    raise ValueError("Missing key '{}'".format(k))
            for k, t in [("type", int), ("args", dict)]:
                if not isinstance(json_dict[k], t):
                    raise ValueError("Key '{}' should be a {}".format(k, t))

            return HttpFsRequest(
                json_dict["type"],
                json_dict["args"]
            )
        except Exception as e:
            raise ValueError("Invalid JSON for {}: '{}'".format(__class__, e))

    def as_dict(self):
        # See HttpFsRequest.schema.json
        return {
            "type": self._type,
            "args": self._args
        }
