import os
import pathlib

import OpenSSL.crypto
from OpenSSL.crypto import PKey, TYPE_RSA, FILETYPE_PEM


class RSAKey(PKey):
    def __init__(self, bits=2048):
        """
        :param bits: Number of key bits
        """
        super().__init__()
        self.generate_key(TYPE_RSA, bits)

    def __bytes__(self):
        return OpenSSL.crypto.dump_privatekey(FILETYPE_PEM, self)

    def write(self, file_name):
        """
        Securely writes the RSAKey to file_name
        :param file_name: The file to write to
        """
        # Make sure content is never written before the current user has
        # exclusive access
        if os.path.exists(file_name):
            os.remove(file_name)
        pathlib.Path(file_name, mode=0o600).touch()

        with open(file_name, 'wb') as f:
            f.write(bytes(self))
