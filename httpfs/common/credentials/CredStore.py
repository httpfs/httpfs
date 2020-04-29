import os
from abc import ABC, abstractmethod
from binascii import hexlify


class CredStore(ABC):
    @abstractmethod
    def add_cred(self):
        pass

    @abstractmethod
    def delete_cred(self, cred):
        pass

    @abstractmethod
    def has_cred(self, cred):
        pass

    @staticmethod
    def generate_cred():
        return hexlify(os.urandom(16)).decode("utf-8")

    @staticmethod
    def from_file(file_str):
        raise NotImplementedError("Subclasses must override from_file()")
