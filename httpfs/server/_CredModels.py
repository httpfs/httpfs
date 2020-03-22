from abc import ABC, abstractmethod
from binascii import hexlify
from os import urandom


class _Cred():

    def __init__(self, key: str = ""):
        if key == "":
            self.key = hexlify(urandom(256))
        else:
            self.key = key

    def __eq__(self, other: _Cred) -> bool:
        return isinstance(self, _Cred) and self.key == other.key

    @staticmethod
    def generateCred() -> _Cred:
        return _Cred()


class _CredStore(ABC):
    @abstractmethod
    def storeCred(self, cred: _Cred):
        pass

    @abstractmethod
    def deleteCred(self, cred: _Cred):
        pass

    @abstractmethod
    def hasCred(self, cred: _Cred) -> bool:
        pass
