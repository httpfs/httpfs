from .CredModels import Cred, CredStore
from threading import RLock
from os.path import exists
from os import chmod
from typing import Optional


class TextCredStore(CredStore):
    def __init__(self, file_path: str = './creds'):
        self.filePath = file_path
        if not exists(file_path):
            file = open(file_path, 'w')
            file.close()
            # Only allow the user on the server to read and write to the keys
            # file
            chmod(file_path, 0o600)
        super().__init__()

    def storeCred(self, cred: Cred):
        lock = RLock()
        with lock, open(self.filePath, 'a') as file:
            if not self.has_cred(cred):
                file.write(str(cred) + '\n')

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
            lines = ['$'.join(dbCred) for dbCred in lines]
            with open(self.filePath, 'w') as file:
                file.writelines(lines)

    def getCred(self, host: str, bearer: str) -> Optional[Cred]:
        lock = RLock()
        with lock, open(self.filePath, 'r') as file:
            for line in file.readlines():
                db_cred = [part.strip() for part in line.split('$')]
                if db_cred[0] == host and db_cred[1] == bearer:
                    return Cred(db_cred[0], db_cred[1], db_cred[2])
        return None

    def has_cred(self, cred: Cred) -> bool:
        lock = RLock()
        with lock, open(self.filePath, 'r') as file:
            for line in file.readlines():
                if line.strip() == str(cred):
                    return True
        return False
