class HttpFsResponse:
    """
    Class representing a filesystem operation result with JSON
    serialization/deserialization methods
    """
    ERR_NONE = 0

    def __init__(self, error_no=ERR_NONE, response_data=dict()):
        """
        Class cooresponding to the schema
        https://raw.githubusercontent.com/httpfs/httpfs/master/HttpFsResponse.schema.json
        :param error_no: Zero for success, https://python.readthedocs.io/en/latest/library/errno.html on error
        :param response_data: Bytes representing data associated with the response body
        """
        # TODO: API Key
        self._error_no = error_no
        self._response_data = response_data

    def is_error(self):
        return self._error_no != 0

    def get_error_no(self):
        return self._error_no

    def get_data(self):
        return self._response_data

    def set_data(self, data):
        self._response_data = data

    def set_err_no(self, err_no):
        self._error_no = err_no

    @staticmethod
    def from_dict(json_dict):
        try:
            for k in ["error_no", "response_data"]:
                if k not in json_dict.keys():
                    raise ValueError("Missing key '{}'".format(k))
            for k, t in [("error_no", int), ("response_data", dict)]:
                if not isinstance(json_dict[k], t):
                    raise ValueError("Key '{}' should be a {}".format(k, t))

            return HttpFsResponse(
                json_dict["error_no"],
                response_data=json_dict["response_data"]
            )
        except Exception as e:
            raise ValueError("Invalid JSON for {}: '{}'".format(__class__, e))

    def as_dict(self):
        # See HttpFsRequest.schema.json
        return {
            "error_no": self._error_no,
            "response_data": self._response_data
        }
