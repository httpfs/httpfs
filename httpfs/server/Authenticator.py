from httpfs.common.CredModels import Cred, CredStore


class Authenticator:
    def __init__(self, credStore: CredStore):
        self.credStore = credStore

    def isCredValid(self, cred: Cred) -> bool:
        return self.credStore.hasCred(cred)

    def addValidCred(self, cred: Cred):
        self.credStore.storeCred(cred)

    def removeValidCred(self, cred: Cred):
        self.credStore.deleteCred(cred)
