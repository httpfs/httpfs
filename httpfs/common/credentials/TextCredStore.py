import json
import os
import pathlib

from .CredStore import CredStore


class TextCredStore(CredStore):
    def __init__(self, file_path):
        self._file = file_path
        self._key_set = set()

        # If doesn't exist, create with RW for current user only
        if not os.path.exists(file_path):
            pathlib.Path(file_path).touch(0o600)
            self._save_store()
        else:
            self._load_store()

    def _load_store(self):
        with open(self._file) as f:
            self._key_set = set(json.load(f))

    def _save_store(self):
        with open(self._file, 'w') as f:
            json.dump(list(self._key_set), f)

    def add_cred(self):
        new_cred = TextCredStore.generate_cred()
        self._key_set.add(new_cred)
        self._save_store()
        return new_cred

    def delete_cred(self, cred):
        if cred in self._key_set:
            self._key_set.remove(cred)
            self._save_store()

    def has_cred(self, cred):
        return cred in self._key_set

    def get_creds(self):
        return list(self._key_set)

    @staticmethod
    def from_file(file_path):
        new_store = TextCredStore(file_path)
        new_store._load_store()
        return new_store
