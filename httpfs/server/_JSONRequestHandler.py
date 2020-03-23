import json
from http.server import BaseHTTPRequestHandler


class _JSONRequestHandler(BaseHTTPRequestHandler):
    ERR_INVALID_CONTENT_TYPE = "Incompatible Content-Type"
    ERR_UNAUTHORIZED = "Client not authorized"
    ERR_INVALID_JSON = "Invalid JSON sent: '{}'"
    ERR_INVALID_REQ_TYPE = "HTTP method not supported"
    ERR_UNKNOWN = "Unknown error"
    ERR_CONTENT_LENGTH = "Content-Length was 0 or was not set"

    protocol_version = "HTTP/1.1"
    default_request_version = "HTTP/1.1"

    @staticmethod
    def _dict_to_json(dict_obj):
        try:
            return json.dumps(dict_obj)
        except json.JSONDecodeError as e:
            return e.msg

    @staticmethod
    def _json_to_dict(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return e.msg

    def on_valid_request(self, request_dict):
        """
        To be implemented by extending classes
        :param request_dict: The valid object sent by the client
        """
        pass

    def on_invalid_request(self, err_msg):
        """
        To be implemented by extending classes
        :param err_msg: Error str explaining why request was invalid
        """
        pass

    def do_GET(self):
        """
        Called when a GET request comes in
        :return:
        """
        return self._validate_request()

    def do_POST(self):
        """
        Called when a POST request comes in
        :return:
        """
        return self._validate_request()

    # Invalid request methods
    # def do_HEAD(self):
    #     return self.on_invalid_request(_JSONRequestHandler.ERR_INVALID_REQ_TYPE)

    # do_PUT = do_HEAD
    # do_DELETE = do_HEAD
    # do_CONNECT = do_HEAD
    # do_OPTIONS = do_HEAD
    # do_TRACE = do_HEAD
    # do_PATCH = do_HEAD

    def _validate_request(self):
        """
        Called when any valid request comes in
        """
        content_len = 0

        # Check for JSON request
        json_sent = (
            "Content-Type" in self.headers and
            self.headers["Content-Type"].startswith("application/json")
        )

        if not json_sent:
            return self.on_invalid_request(_JSONRequestHandler.ERR_INVALID_CONTENT_TYPE)

        # Check for Content-Length
        length_sent = "Content-Length" in self.headers

        if length_sent:
            content_len = int(self.headers["Content-Length"])

        if not length_sent or content_len <= 0:
            return self.on_invalid_request(_JSONRequestHandler.ERR_CONTENT_LENGTH)

        # Parse request
        request_str = self.rfile.read(content_len).decode("utf-8")
        request_json = _JSONRequestHandler._json_to_dict(request_str)

        if isinstance(request_json, dict):
            # This is the only successful outcome
            return self.on_valid_request(request_json)
        else:
            return self.on_invalid_request(_JSONRequestHandler.ERR_INVALID_JSON.format(request_json))

    def send_json_response(self, status_code, response_dict):
        """
        Sends the given dict as a json response
        :param status_code: Integer HTTP status code to send
        :param response_dict: The response JSON object
        """
        res_json_bytes = _JSONRequestHandler._dict_to_json(
            response_dict
        ).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(res_json_bytes))
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(res_json_bytes)
