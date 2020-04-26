from httpfs.client import HttpFsClient

HOSTNAME = "test-host"
PORT = 8080
CRED = "fake-cred-as-str"
EXPECTED_URL = "http://{}:{}".format(HOSTNAME, PORT)


def test_constructor():
    client = HttpFsClient(
        HOSTNAME,
        PORT,
        CRED,
        ca_file=None
    )

    assert client.server_hostname == HOSTNAME
    assert client._server_url == EXPECTED_URL
    assert client._cred == CRED
