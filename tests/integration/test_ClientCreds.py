import subprocess as sp
import os
import shlex

from httpfs.client import HttpFsClient
from httpfs.common import TextCredStore, Cred, HttpFsRequest, HttpFsResponse

CRED_STORE_FILE = "./creds"
CLIENT_CRED_STORE_FILE = "./client-creds"


def test_api_key():
    if os.path.exists(CRED_STORE_FILE):
        os.remove(CRED_STORE_FILE)

    # Test that cli correctly generates an API key
    cli_result = sp.run(
        shlex.split("bin/httpfs-cli add-api-key localhost test-user"),
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
    host, bearer, api_key = api_key_str.strip().split("$")

    api_key_cred = Cred(host, bearer, api_key)
    assert cred_store.has_cred(api_key_cred)

    # Create an httpfs client store
    client_cred_store = Cred(host, bearer, api_key)
    client = HttpFsClient("localhost", 8080, client_cred_store)

    # Mock sending a request
    def fake_send_request(request_type, **kwargs):
        # This is how the real method forms a request object
        request = HttpFsRequest(
            request_type,
            kwargs,
            client._cred
        )
        request_as_dict = request.as_dict()

        # Make sure the API has passed through the client to the request
        assert request_as_dict["auth"] == api_key_str

        resp = HttpFsResponse()
        resp._response_data["target"] = "/some/link/real/path"
        return resp

    client._send_request = fake_send_request
    client.readlink("/some/link")

    os.remove(CRED_STORE_FILE)
