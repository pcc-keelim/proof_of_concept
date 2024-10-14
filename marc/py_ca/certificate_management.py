import os
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class CertificateAuthority:
    def __init__(self, key_size, validity_years, country, state, org_name, passphrase):
        """
        Initialize the Certificate Authority with the given parameters.
        """
        self.key_size = key_size
        self.validity_years = validity_years
        self.country = country
        self.state = state
        self.org_name = org_name
        self.passphrase = passphrase.encode() if passphrase else None
        self.private_key = None
        self.ca_cert = None

    def generate_certificate_authority(self, directory):
        """
        Generate the CA's private key and self-signed certificate.
        Save them to the specified directory.
        """
        # Generate private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )

        # Build subject and issuer name
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.org_name),
            x509.NameAttribute(NameOID.COMMON_NAME, f"{self.org_name} CA"),
        ])

        # Build certificate
        self.ca_cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365 * int(self.validity_years))
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        ).sign(self.private_key, hashes.SHA256())

        # Save private key and certificate
        # ca_dir = os.path.join(directory, 'ca')
        os.makedirs(directory, exist_ok=True)

        # Save private key encrypted with passphrase
        key_path = os.path.join(directory, 'ca.key.pem')
        with open(key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm = serialization.NoEncryption() if not self.passphrase else serialization.BestAvailableEncryption(self.passphrase)
            ))

        # Save certificate
        cert_path = os.path.join(directory, 'ca.cert.pem')
        with open(cert_path, 'wb') as f:
            f.write(self.ca_cert.public_bytes(serialization.Encoding.PEM))

    @classmethod
    def from_file(cls, directory, passphrase):
        """
        Load the CA's private key and certificate from the specified directory.
        """
        ca_dir = directory
        key_path = os.path.join(ca_dir, 'ca.key.pem')
        cert_path = os.path.join(ca_dir, 'ca.cert.pem')

        # Load private key
        with open(key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=passphrase.encode() if passphrase else None
            )

        # Load certificate
        with open(cert_path, 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())

        # Create an instance of CertificateAuthority without regenerating keys
        instance = cls(
            key_size=private_key.key_size,
            validity_years=(ca_cert.not_valid_after - ca_cert.not_valid_before).days // 365,
            country=ca_cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,
            state=ca_cert.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value,
            org_name=ca_cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value,
            passphrase=passphrase
        )
        instance.private_key = private_key
        instance.ca_cert = ca_cert

        return instance


class ServerClientCertificate:
    def __init__(self, ca, cert_type, cert_name, key_size, validity_days, country, state, org_name, san_list):
        """
        Initialize the server or client certificate parameters.
        """
        self.ca = ca
        self.cert_type = cert_type  # 'server' or 'client'
        self.cert_name = cert_name
        self.key_size = key_size
        self.validity_days = validity_days
        self.country = country
        self.state = state
        self.org_name = org_name
        self.san_list = san_list
        self.private_key = None
        self.certificate = None

    def generate_certificate(self, directory):
        """
        Generate the certificate and private key, sign it with the CA, and save to files.
        """
        # Generate private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )

        # Build subject name
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.org_name),
            x509.NameAttribute(NameOID.COMMON_NAME, self.san_list[0]),
        ])

        # Build certificate
        cert_builder = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.ca.ca_cert.subject
        ).public_key(
            self.private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow() - datetime.timedelta(days=1)
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=int(self.validity_days))
        )

        # Add SAN extension
        san = x509.SubjectAlternativeName([
            x509.DNSName(name) for name in self.san_list
        ])
        cert_builder = cert_builder.add_extension(
            san,
            critical=False
        )

        # Add extended key usages
        if self.cert_type == 'server':
            eku = x509.ExtendedKeyUsage([
                ExtendedKeyUsageOID.SERVER_AUTH
            ])
        elif self.cert_type == 'client':
            eku = x509.ExtendedKeyUsage([
                ExtendedKeyUsageOID.CLIENT_AUTH
            ])
        else:
            raise ValueError("cert_type must be 'server' or 'client'")
        cert_builder = cert_builder.add_extension(
            eku,
            critical=False
        )

        # Sign certificate with CA's private key
        self.certificate = cert_builder.sign(
            private_key=self.ca.private_key,
            algorithm=hashes.SHA256()
        )

        # Save private key and certificate
        os.makedirs(directory, exist_ok=True)

        key_path = os.path.join(directory, f'{self.cert_name}.key.pem')
        with open(key_path, 'wb') as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        cert_path = os.path.join(directory, f'{self.cert_name}.cert.pem')
        with open(cert_path, 'wb') as f:
            f.write(self.certificate.public_bytes(serialization.Encoding.PEM))

# Assuming arguments will be passed via sys.argv
def main():
    request_type = os.environ.get("REQUEST_TYPE")
    ca_storage_path = os.environ.get("CA_STORAGE_PATH")
    passphrase = os.environ.get("CA_PASSPHRASE")
    validity_years = os.environ.get("CA_VALIDITY_YEARS")
    org_name = os.environ.get("CA_ORG_NAME")
    state = os.environ.get("CA_STATE")
    # country = os.environ.get("CA_COUNTRY")
    country = 'US'

    if request_type == "generate_ca":
        # Generate CA if not already present in the folder
        if os.path.exists(ca_storage_path) and len(os.listdir(ca_storage_path)) > 0:
            print(f"CA already exists at {ca_storage_path}. Skipping CA creation.")
        else:
            ca = CertificateAuthority(
                key_size=4096,
                validity_years=validity_years,
                country="US",
                state=state,
                org_name=org_name,
                passphrase=passphrase
            )
            ca.generate_certificate_authority(directory=ca_storage_path)
            print(f"CA created at {ca_storage_path}")

    elif request_type == "generate_server_cert":
        # Check if CA directory exists
        if not os.path.exists(ca_storage_path):
            raise FileNotFoundError(f"CA directory {ca_storage_path} does not exist")

        cert_name = os.environ.get("CERT_NAME", "server_cert")
        san_list = os.environ.get("SAN_LIST", "").split(',')
        validity_days = os.environ.get("CERT_VALIDITY_DAYS", 365)
        
        # Generate the ClickHouse certificate in a subfolder within the CA folder
        server_cert_folder = os.path.join(ca_storage_path, "certificates", f"server_{cert_name}")
        os.makedirs(server_cert_folder, exist_ok=True)
        
        ca = CertificateAuthority.from_file(ca_storage_path, passphrase=passphrase)
        clickhouse_cert = ServerClientCertificate(
            ca=ca,
            cert_type="server",
            cert_name=cert_name,
            key_size=2048,  # or 4096 if preferred
            validity_days=validity_days,
            country=country,
            org_name=org_name,
            state=state,
            san_list=san_list
        )
        clickhouse_cert.generate_certificate(server_cert_folder)
        print(f"Server certificate generated in {server_cert_folder}")

    else:
        print("Invalid REQUEST_TYPE. Must be 'generate_ca' or 'generate_server_cert'.")


if __name__ == "__main__":
    main()
