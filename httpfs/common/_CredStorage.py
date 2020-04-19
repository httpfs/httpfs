from ._CredModels import _Cred, _CredStore
from threading import RLock
from os.path import exists
from os import chmod
from typing import Optional


class _TextCredStore(_CredStore):
    def __init__(self, filePath: str = './creds'):
        self.filePath = filePath
        if not exists(filePath):
            file = open(filePath, 'w')
            file.close()
            # Only allow the user on the server to read and write to the keys file
            chmod(filePath, 0o600)
        super().__init__()

    def storeCred(self, cred: _Cred):
        lock = RLock()
        with lock, open(self.filePath, 'a') as file:
            if not self.hasCred(cred):
                file.write(cred.str() + '\n')

    def deleteCred(self, host: str, bearer: str):
        lock = RLock()
        with lock:
            lines = []
            with open(self.filePath, 'r') as file:
                lines = file.readlines()
            lines = map(lambda line: line.split('$'), lines)
            lines = filter(
                (lambda dbCred: not (
                    dbCred[0] == host and dbCred[1] == bearer)),
                lines)
            lines = map(lambda dbCred: '$'.join(dbCred))
            with open(self.filePath, 'w') as file:
                file.writelines(lines)

    def getCred(self, host: str, bearer: str) -> Optional[_Cred]:
        lock = RLock()
        with lock, open(self.filePath, 'r') as file:
            for line in file.readline():
                dbCred = line.split('$')
                if dbCred[0] == host and dbCred[1] == bearer:
                    return _Cred(dbCred[0], dbCred[1], dbCred[2])
        return None

    def hasCred(self, cred: _Cred) -> bool:
        lock = RLock()
        with lock, open(self.filePath, 'r') as file:
            for line in file.readline():
                if line == cred.str():
                    return True
        return False
