from _CredModels import _Cred, _CredStore
import threading


class _TextCredStore(_CredStore):
    def __init__(self, filePath: str):
        self.filePath = filePath

    def storeCred(self, cred: _Cred):
        lock = threading.RLock()
        with lock, open(self.filePath, 'a') as file:
            file.write(cred.key + '\n')

    def deleteCred(self, cred: _Cred):
        pass

    def hasCred(self, cred: _Cred) -> bool:
        pass
