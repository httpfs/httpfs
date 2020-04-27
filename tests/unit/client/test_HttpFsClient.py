import base64
import json
import os
import sys
import unittest
import unittest.mock as mock
from unittest.mock import MagicMock

from httpfs.client import HttpFsClient
from httpfs.common import HttpFsRequest, HttpFsResponse

HOSTNAME = "test-host"
PORT = 8080
CRED = "fake-cred-as-str"
EXPECTED_URL = "http://{}:{}".format(HOSTNAME, PORT)

FAKE_API_KEY = "1234"
FAKE_REQ_TYPE = HttpFsRequest.OP_ACCESS
FAKE_REQ_ARGS = {
    "key": "val",
    "key2": "val2"
}
FAKE_POST_REQ = {
    "type": FAKE_REQ_TYPE,
    "args": FAKE_REQ_ARGS,
    "auth": CRED
}

def test_constructor_without_ssl():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    assert client.server_hostname == HOSTNAME
    assert client._server_url == EXPECTED_URL
    assert client._cred == CRED

@mock.patch("os.path.exists", return_value=True)
def test_constructor_with_ssl(mocker):
    client_w_ca = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file="test-file.crt"
    )

    assert client_w_ca.server_hostname == HOSTNAME
    assert client_w_ca._cred == CRED
    assert client_w_ca._server_url.startswith("https")


def test_send_request():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    # Fake response from the server
    fake_response = MagicMock()
    fake_response.raise_for_status = MagicMock(return_value=None)
    fake_response.headers = {
        "Content-Type": "application/json",
        "Server": "HttpFs"
    }
    fake_response.json = MagicMock(return_value={ 
        "error_no": HttpFsResponse.ERR_NONE, 
        "response_data": {} 
    })

    # Fake POST request method
    def fake_post(server_url, json=None, allow_redirects=False, timeout=10, stream=True):
        assert server_url == client._server_url
        assert json == FAKE_POST_REQ
        return fake_response

    # Fake requests.session
    fake_session = MagicMock()
    fake_session.post = fake_post

    client._http_keepalive_session = fake_session
    client._send_request(FAKE_REQ_TYPE, **FAKE_REQ_ARGS)

def test_access():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_mode = 0o600

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_ACCESS
        for required_key in ["uid", "gid"]:
            assert required_key in kwargs.keys()
        assert kwargs["path"] == fake_path
        assert kwargs["mode"] == fake_mode
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.access(fake_path, fake_mode)

def test_create():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_mode = 0o600

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_CREATE
        for required_key in ["uid", "gid"]:
            assert required_key in kwargs.keys()
        assert kwargs["path"] == fake_path
        assert kwargs["mode"] == fake_mode
        resp = HttpFsResponse()
        resp._response_data["file_descriptor"] = 0
        return resp

    client._send_request = fake_send_request
    client.create(fake_path, fake_mode)

def test_chmod():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_mode = 0o600

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_CHMOD
        for required_key in ["uid", "gid"]:
            assert required_key in kwargs.keys()
        assert kwargs["path"] == fake_path
        assert kwargs["mode"] == fake_mode
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.chmod(fake_path, fake_mode)

def test_chown():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_CHOWN
        assert kwargs["path"] == fake_path
        assert kwargs["uid"] == 2222
        assert kwargs["gid"] == 0
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.chown(fake_path, 2222, 0)

def test_flush():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_fd = 1234

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_FLUSH
        assert kwargs["file_descriptor"] == fake_fd
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.flush(fake_path, fake_fd)

def test_fsync():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_fd = 1234
    fake_ds = True

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_FSYNC
        assert kwargs["file_descriptor"] == fake_fd
        assert kwargs["datasync"] == fake_ds
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.fsync(fake_path, fh=fake_fd, datasync=fake_ds)

def test_getattr():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_GET_ATTR
        assert kwargs["path"] == fake_path
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.getattr(fake_path)

def test_link():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_source = "/some/source"
    fake_target = "/some/target"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_LINK
        assert kwargs["target"] == fake_target
        assert kwargs["source"] == fake_source
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.link(fake_target, fake_source)

def test_mkdir():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_mode = 0o644

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_MKDIR
        assert kwargs["path"] == fake_path
        assert kwargs["mode"] == fake_mode
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.mkdir(fake_path, fake_mode)


def test_mknod():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_mode = 0o644
    fake_dev = False

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_MKNOD
        assert kwargs["path"] == fake_path
        assert kwargs["mode"] == fake_mode
        assert kwargs["dev"] == fake_dev
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.mknod(fake_path, fake_mode, fake_dev)

def test_open():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_flags = 0 | 1 | 2 | 666

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_OPEN
        assert kwargs["path"] == fake_path
        assert kwargs["flags"] == fake_flags
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.open(fake_path, fake_flags)

def test_read():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_offset = 1024
    fake_size = 512
    fake_fd = 0

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_READ
        assert kwargs["file_descriptor"] == fake_fd
        assert kwargs["size"] == fake_size
        assert kwargs["offset"] == fake_offset
        resp = HttpFsResponse()
        resp._response_data["bytes_read"] = bytes()
        return resp

    client._send_request = fake_send_request
    client.read(fake_path, fake_size, fake_offset, fh=fake_fd)

def test_readdir():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_READDIR
        assert kwargs["path"] == fake_path
        resp = HttpFsResponse()
        resp._response_data["dir_listing"] = list()
        return resp

    client._send_request = fake_send_request
    client.readdir(fake_path)

def test_readlink():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_READLINK
        assert kwargs["link_path"] == fake_path
        resp = HttpFsResponse()
        resp._response_data["target"] = ""
        return resp

    client._send_request = fake_send_request
    client.readlink(fake_path)

def test_release():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/"
    fake_fd = 999

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_RELEASE
        assert kwargs["file_descriptor"] == fake_fd
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.release(fake_path, fh=fake_fd)

def test_rename():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_old_path = "/old-path"
    fake_new_path = "/new-path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_RENAME
        assert kwargs["old_path"] == fake_old_path
        assert kwargs["new_path"] == fake_new_path
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.rename(fake_old_path, fake_new_path)

def test_rmdir():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_RM_DIR
        assert kwargs["path"] == fake_path
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.rmdir(fake_path)

def test_statfs():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_STAT_FS
        assert kwargs["path"] == fake_path
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.statfs(fake_path)

def test_symlink():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_source = "/some/source"
    fake_target = "/some/target"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_SYMLINK
        assert kwargs["target"] == fake_target
        assert kwargs["source"] == fake_source
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.symlink(fake_target, fake_source)

def test_truncate():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_len = 16

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        assert request_type == HttpFsRequest.OP_TRUNCATE
        assert kwargs["path"] == fake_path
        assert kwargs["length"] == fake_len
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.truncate(fake_path, fake_len)

def test_unlink():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_UNLINK
        assert kwargs["path"] == fake_path
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.unlink(fake_path)

def test_utimens():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_times = (0, 0)

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_UTIMENS
        assert kwargs["path"] == fake_path
        assert kwargs["times"] == fake_times
        return HttpFsResponse()

    client._send_request = fake_send_request
    client.utimens(fake_path, times=fake_times)

def test_write():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    fake_path = "/some/path"
    fake_data = b"This is some bytes"
    fake_offset = 1024
    fake_fd = 0

    # Fake _send_request
    def fake_send_request(request_type, **kwargs):
        for arg in ["uid", "gid"]:
            assert arg in kwargs.keys()
        assert request_type == HttpFsRequest.OP_WRITE
        assert kwargs["file_descriptor"] == fake_fd
        assert kwargs["data"] == base64.standard_b64encode(fake_data).decode("utf-8")
        assert kwargs["offset"] == fake_offset
        resp = HttpFsResponse()
        resp._response_data["bytes_written"] = 10
        return resp

    client._send_request = fake_send_request
    client.write(fake_path, fake_data, fake_offset, fh=fake_fd)
