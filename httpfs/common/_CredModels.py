from abc import ABC, abstractmethod
from binascii import hexlify
from os import urandom


class _Cred():

    def __init__(self, host: str, bearer: str, key: str):
        self.host = host
        self.bearer = bearer
        self.key = key

    def __eq__(self, other):
        return isinstance(self, _Cred) and self.host == other.host and self.bearer == other.bearer and self.key == other.key

    def __str__(self):
        return '{}${}${}'.format(self.host, self.bearer, self.key)


class _CredStore(ABC):
    @abstractmethod
    def storeCred(self, cred: _Cred):
        pass

    @abstractmethod
    def deleteCred(self, host: str, bearer: str):
        pass

    @abstractmethod
    def getCred(self, host: str, bearer: str) -> _Cred:
        pass

    @abstractmethod
    def hasCred(self, cred: _Cred) -> bool:
        pass
