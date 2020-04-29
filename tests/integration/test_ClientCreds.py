import subprocess as sp
import os
import shlex
from unittest.mock import MagicMock

from httpfs.client import HttpFsClient
from httpfs.common import TextCredStore, HttpFsRequest, HttpFsResponse

CRED_STORE_FILE = "./creds.json"

def test_api_key():
    if os.path.exists(CRED_STORE_FILE):
        os.remove(CRED_STORE_FILE)

    # Test that cli correctly generates an API key
    cli_result = sp.run(
        shlex.split("bin/httpfs-cli add-api-key {}".format(CRED_STORE_FILE)),
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        env=os.environ
    )
    try:
        assert cli_result.returncode == 0
    except:
        raise AssertionError(
            "[API Key Generation Failed] {}".format(
                cli_result.stderr.decode("utf-8").strip()
            )
        )

    # Make sure cli correctly populates the new API key in the keystore
    cred_store = TextCredStore(file_path=CRED_STORE_FILE)

    api_key_str = cli_result.stdout.decode("utf-8").strip()
    assert cred_store.has_cred(api_key_str)

    client = HttpFsClient("localhost", 8080, api_key=api_key_str)

    # Mock sending a request
    FAKE_PATH = "/some/link"

    # Fake response from the server
    fake_response = MagicMock()
    fake_response.raise_for_status = MagicMock(return_value=None)
    fake_response.headers = {
        "Content-Type": "application/json",
        "Server": "HttpFs"
    }
    fake_response.json = MagicMock(return_value={
        "error_no": HttpFsResponse.ERR_NONE,
        "response_data": {
            "target": FAKE_PATH
        }
    })

    def fake_post(server_url, **kwargs):
        assert server_url == client._server_url
        assert "Authorization" in kwargs["headers"] and kwargs["headers"]["Authorization"] == api_key_str
        assert kwargs["json"]["type"] == HttpFsRequest.OP_READLINK
        assert kwargs["json"]["args"]["link_path"] == FAKE_PATH
        return fake_response

    client._http_keepalive_session.post = fake_post
    client.readlink("/some/link")

    os.remove(CRED_STORE_FILE)
