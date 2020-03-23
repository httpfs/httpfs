from ._CredModels import _Cred, _CredStore
from threading import RLock
from typing import List
from os.path import exists
from os import chmod


class _TextCredStore(_CredStore):
    def __init__(self, filePath: str):
        self.filePath = filePath
        if not exists(filePath):
            file = open(filePath, 'w')
            file.close()
            # Only allow the user on the server to read and write to the keys file
            chmod(filePath, 0o600)

    def storeCred(self, cred: _Cred):
        lock = RLock()
        with lock, open(self.filePath, 'a') as file:
            if not self.hasCred(cred):
                file.write(cred.key + '\n')

    def deleteCred(self, cred: _Cred):
        lock = RLock()
        with lock:
            contents = ''
            with open(self.filePath, 'r') as file:
                contents = file.read()
            contents = contents.replace(cred.key + '\n', '')
            with open(self.filePath, 'w') as file:
                file.write(contents)

    def hasCred(self, cred: _Cred) -> bool:
        lock = RLock()
        with lock, open(self.filePath, 'r') as file:
            for line in file.readline():
                if line == cred.key:
                    return True
        return False
