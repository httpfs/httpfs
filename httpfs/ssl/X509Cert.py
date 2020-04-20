import os
import socket
import OpenSSL

from datetime import datetime
from OpenSSL.crypto import X509, X509Extension, FILETYPE_PEM


class X509Cert(X509):
    def __init__(self, rsa_key, country, state, locality, org, cn, issuer=None):
        """
        :param rsa_key: Corresponding key for the certificate
        :param country: Cert country
        :param state: Cert state
        :param locality: Cert locality
        :param org: Cert organization
        :param cn: Cert common name
        :param issuer: OpenSSL.crypto.X509Name for the certificate issuer
        """
        super().__init__()
        self.set_pubkey(rsa_key)
        self.set_notBefore(X509Cert.get_now())
        self.set_notAfter(X509Cert.get_year_from_now())
        self.set_serial_number(int.from_bytes(os.urandom(8), "big"))
        crt_subject = self.get_subject()
        crt_subject.C = country
        crt_subject.ST = state
        crt_subject.L = locality
        crt_subject.O = org
        crt_subject.CN = cn

        if issuer is None:
            issuer = crt_subject
            self.add_extensions([X509Extension(
                "basicConstraints".encode("utf-8"),
                critical=True,
                value="CA:TRUE".encode("utf-8")
            )])
        self.set_issuer(issuer)
        self._add_sans()

    def _add_sans(self):
        """
        Adds Subject Alternate names for the certificate based on the
        server's current IP address and DNS name
        """
        current_ip = X509Cert.get_current_ip()
        current_dns_name = socket.gethostbyaddr(current_ip)[0]
        sans = set()
        sans.add("DNS:*.{}".format(socket.getfqdn()))
        sans.add("DNS:{}".format(current_dns_name))
        sans.add("DNS:*.{}".format(current_dns_name))
        sans.add("IP:{}".format(current_ip))
        sans = list(sans)

        self.add_extensions([X509Extension(
            "subjectAltName".encode("utf-8"),
            critical=False,
            value=",".join(sans).encode("utf-8")
        )])

    def __bytes__(self):
        return OpenSSL.crypto.dump_certificate(FILETYPE_PEM, self)

    def write(self, file_name, chain=()):
        """
        Writes the X509Cert to file_name
        :param file_name: File name to write to
        :param chain: Additional X509Certs to include in the file
        """
        with open(file_name, 'wb') as f:
            f.write(bytes(self))
        for parent_crt in chain:
            with open(file_name, 'ab') as f:
                f.write(bytes(parent_crt))

    def sign(self, pkey):
        """
        Signs the cert using an RSAKey object
        :param pkey: RSAKey used to sign the certificate
        """
        super().sign(pkey, "sha256")

    @staticmethod
    def get_now():
        """
        :return: The current UTC timestamp in ASN.1 (OpenSSL) format
        """
        return datetime.utcnow().strftime("%Y%m%d%H%M%SZ").encode("utf-8")

    @staticmethod
    def get_year_from_now():
        """
        :return: A year from now's UTC timestamp in ASN.1 (OpenSSL) format
        """
        now = datetime.utcnow()
        year_out = now.replace(year=(now.year + 1))
        return year_out.strftime("%Y%m%d%H%M%SZ").encode("utf-8")

    @staticmethod
    def get_current_ip():
        """
        :return: The IP address that is used to connect to 8.8.8.8
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 1))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
