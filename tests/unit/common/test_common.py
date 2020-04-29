import os
from httpfs.common import TextCredStore

TEST_FILE = "test-file.json"

def test_TextCredStore():
    repo = TextCredStore("test-file.json")
    assert os.path.exists(TEST_FILE)
    assert os.access(repo._file, os.R_OK)
    assert os.access(repo._file, os.W_OK)

    key = repo.add_cred()
    assert key in repo._key_set

    os.remove(TEST_FILE)
