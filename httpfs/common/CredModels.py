import os
from abc import ABC, abstractmethod
from binascii import hexlify


class Cred:

    def __init__(self, host: str, bearer: str, key: str):
        self.host = host
        self.bearer = bearer
        self.key = key

    def __eq__(self, other):
        return isinstance(self, Cred) and self.host == other.host and self.bearer == other.bearer and self.key == other.key

    def __str__(self):
        return '{}${}${}'.format(self.host, self.bearer, self.key)


class CredStore(ABC):
    @abstractmethod
    def storeCred(self, cred: Cred):
        pass

    @abstractmethod
    def deleteCred(self, host: str, bearer: str):
        pass

    @abstractmethod
    def getCred(self, host: str, bearer: str) -> Cred:
        pass

    @abstractmethod
    def hasCred(self, cred: Cred) -> bool:
        pass

    @staticmethod
    def generate_key():
        return hexlify(os.urandom(256)).decode("utf-8")

