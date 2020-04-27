import os
from httpfs.common import HttpFsRequest, HttpFsResponse
from httpfs.common import Cred, CredStore, TextCredStore

def test_TextCredStore():
    if os.path.exists("./creds"):
        os.remove("./creds")

    repo = TextCredStore()
    assert os.path.exists(repo.filePath)
    assert os.access(repo.filePath, os.R_OK) 
    assert os.access(repo.filePath, os.W_OK)
    
    key = repo.generate_key()
    cred = Cred('localhost', 'ur mom', key)
    repo.storeCred(cred)
    assert repo.has_cred(cred)
    print(repo.getCred(cred.host, cred.bearer))
    print(cred)
    assert repo.getCred(cred.host, cred.bearer) == cred
    
    repo.deleteCred(cred.host, cred.bearer)
    assert not repo.has_cred(cred)
    assert repo.getCred(cred.host, cred.bearer) == None
    os.remove(repo.filePath)