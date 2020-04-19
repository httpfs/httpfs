from httpfs.common._CredModels import _Cred, _CredStore


class _Authenticator():
    def __init__(self, credStore: _CredStore):
        self.credStore = credStore

    def isCredValid(self, cred: _Cred) -> bool:
        return self.credStore.hasCred(cred)

    def addValidCred(self, cred: _Cred):
        self.credStore.storeCred(cred)

    def removeValidCred(self, cred: _Cred):
        self.credStore.deleteCred(cred)
