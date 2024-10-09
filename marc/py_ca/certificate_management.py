import os # pylint: disable=missing-module-docstring
from datetime import datetime, timedelta
import sys
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

class CertificateBase:
    """
    Base class for Certificate handling, providing common methods for key generation,
    certificate creation, and saving certificates and keys.
    """

    def generate_rsa_key(self, key_size=4096):
        """
        Generates an RSA private key.

        Args:
            key_size (int): Size of the RSA key. Defaults to 2048 bits.

        Returns:
            rsa.RSAPrivateKey: The generated RSA private key.
        """
        return rsa.generate_private_key(public_exponent=65537, key_size=key_size)

    def create_cert(self,
        subject,
        issuer,
        public_key,
        private_key,
        validity_days,
        is_ca=False,
        san_list=None):
        """
        Creates a certificate with the given attributes.

        Args:
            subject (x509.Name): The subject name for the certificate.
            issuer (x509.Name): The issuer name for the certificate.
            public_key (rsa.RSAPublicKey): The public key for the certificate.
            private_key (rsa.RSAPrivateKey): The private key to sign the certificate.
            validity_days (int): Number of days the certificate is valid.
            is_ca (bool): Whether this certificate is for a Certificate Authority.
            san_list (list): List of Subject Alternative Names (SANs) (optional).

        Returns:
            x509.Certificate: The generated certificate.
        """
        builder = x509.CertificateBuilder().subject_name(subject)\
            .issuer_name(issuer)\
            .public_key(public_key)\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=validity_days))

        # If it's a CA, add the Basic Constraints extension
        if is_ca:
            builder = builder.add_extension(
                x509.BasicConstraints(ca=True, path_length=None), critical=True
            )

        # Add SAN if provided (typically for server/client certificates)
        if san_list:
            san_extension = x509.SubjectAlternativeName([x509.DNSName(name) for name in san_list])
            builder = builder.add_extension(san_extension, critical=False)

        # Sign the certificate with the provided private key
        return builder.sign(private_key=private_key, algorithm=hashes.SHA256())

    def create_and_sign_cert(self,
        subject,
        issuer,
        private_key,
        validity_days,
        is_ca=False,
        san_list=None):
        """
        Helper function that combines key generation and certificate creation.
        This will be used by both CA and Server/Client certificates.

        Args:
            subject (x509.Name): The subject name for the certificate.
            issuer (x509.Name): The issuer name for the certificate.
            private_key (rsa.RSAPrivateKey): The private key to sign the certificate.
            validity_days (int): Number of days the certificate is valid.
            is_ca (bool): Whether this certificate is for a Certificate Authority.
            san_list (list): List of Subject Alternative Names (SANs) (optional).

        Returns:
            x509.Certificate: The generated certificate.
        """
        return self.create_cert(
            subject=subject,
            issuer=issuer,
            public_key=private_key.public_key(),
            private_key=private_key,
            validity_days=validity_days,
            is_ca=is_ca,
            san_list=san_list
        )

    def save_cert_and_key(self, cert, private_key, cert_path, key_path, passphrase=None):
        """
        Saves the certificate and private key to the specified paths.

        Args:
            cert (x509.Certificate): The certificate to save.
            private_key (rsa.RSAPrivateKey): The private key to save.
            cert_path (str): Path to save the certificate.
            key_path (str): Path to save the private key.
            passphrase (bytes): Passphrase for encrypting the private key (optional).
        """
        # Save the certificate
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        # Save the private key
        with open(key_path, "wb") as f:
            encryption = serialization.NoEncryption()
            if passphrase:
                encryption = serialization.BestAvailableEncryption(passphrase)

            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=encryption
            ))

    def _generate_subject(self, org_name, state, common_name, country="US"):
        """
        Generates an x509.Name object for the certificate subject or issuer.

        Args:
            org_name (str): Organization name for the certificate.
            state (str): State name for the certificate.
            common_name (str): Common name (CN) for the certificate.
            country (str): Country name for the certificate. Defaults to 'US'.

        Returns:
            x509.Name: The generated subject name.
        """
        return x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

    def _save_to_directory(self, cert, private_key, directory, cert_name, passphrase=None):
        """
        Saves the certificate and private key to the specified directory.

        Args:
            cert (x509.Certificate): The certificate to save.
            private_key (rsa.RSAPrivateKey): The private key to save.
            directory (str): Directory to save the certificate and key.
            cert_name (str): The name for the certificate and key files.
            passphrase (bytes): Passphrase for encrypting the private key (optional).
        """
        if not cert_name:
            raise ValueError("Certificate name is required")

        cert_folder = os.path.join(directory, cert_name)
        if not os.path.exists(cert_folder):
            os.makedirs(cert_folder)
            print(f"Created directory: {cert_folder}")

        cert_path = os.path.join(cert_folder, f"{cert_name}.cert.pem")
        key_path = os.path.join(cert_folder, f"{cert_name}.key.pem")

        self.save_cert_and_key(cert, private_key, cert_path, key_path, passphrase)

class CertificateAuthority(CertificateBase):
    """
    A class to represent a Certificate Authority (CA) for generating 
    and managing CA certificates and keys.

    Attributes:
        key_size (int): Size of the RSA key.
        validity_years (int): Number of years the certificate is valid.
        country (str): Country name for the certificate.
        state (str): State name for the certificate.
        org_name (str): Organization name for the certificate.
        passphrase (str): Passphrase for encrypting the private key.
        encryption_type (str): Type of encryption for the private key.
    """

    def __init__(self,
        key_size=4096,
        validity_years=10,
        country="US",
        state="Utah",
        org_name="pcc_data_engineering",
        passphrase=None,
        encryption_type=None
    ):
        """
        Constructs all the necessary attributes for the CertificateAuthority object.

        Args:
            key_size (int): Size of the RSA key.
            validity_years (int): Number of years the certificate is valid.
            country (str): Country name for the certificate.
            state (str): State name for the certificate.
            org_name (str): Organization name for the certificate.
            passphrase (str): Passphrase for encrypting the private key.
            encryption_type (str): Type of encryption for the private key.
        """
        self.key_size = key_size
        self.validity_years = validity_years
        self.country = country
        self.state = state
        self.org_name = org_name
        self.passphrase = passphrase.encode() if passphrase else None
        self.encryption_type = encryption_type
        self.private_key = None # Private key for the CA
        self.ca_cert = None # CA certificate

    @classmethod
    def from_file(cls, directory, passphrase=None):
        """
        Creates a CertificateAuthority object by loading an existing CA certificate and private key from disk.

        Args:
            directory (str): The directory containing the CA certificate and key.
            passphrase (str): Passphrase for decrypting the private key (optional).

        Returns:
            CertificateAuthority: An instance of the CertificateAuthority class loaded from files.
        """
        ca = cls(passphrase=passphrase)
        cert_path = os.path.join(directory, 'ca.cert.pem')
        key_path = os.path.join(directory, 'ca.key.pem')

        # Load CA certificate
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            raise FileNotFoundError(f"CA certificate or key not found in {directory}")

        with open(cert_path, 'rb') as cert_file:
            ca.ca_cert = x509.load_pem_x509_certificate(cert_file.read())

        # Load private key with or without passphrase
        with open(key_path, 'rb') as key_file:
            ca.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=passphrase.encode() if passphrase else None
            )

        return ca

    def create_key(self):
        """
        Generates the private key for the Certificate Authority (CA).
        """
        self.private_key = self.generate_rsa_key(self.key_size)

    def _create_cert(self):
        """
        Creates the CA certificate with the specified attributes.
        """
        subject = issuer = self._generate_subject(
            org_name=self.org_name,
            state=self.state,
            common_name=f"{self.org_name} Root CA",
            country=self.country
        )

        self.ca_cert = self.create_and_sign_cert(
            subject=subject,
            issuer=subject,  # CA is both the subject and issuer
            private_key=self.private_key,
            validity_days=365 * self.validity_years,
            is_ca=True
        )

    # Use the common save method
    def _save_cert_and_key(self, cert_path):
        self._save_to_directory(self.ca_cert, self.private_key, cert_path, 'ca', self.passphrase)

    def generate_certificate_authority(self, directory):
        """
        Generates the private key for the Certificate 
        Authority (CA) and saves the CA certificate and key.
        """
        self.create_key()
        self._create_cert()
        self._save_cert_and_key(directory)

class ServerClientCertificate(CertificateBase):
    """
    A class to represent a server or client certificate generated by a Certificate Authority (CA).

    Attributes:
        ca (CertificateAuthority): An instance of the CertificateAuthority class.
        cert_type (str): Type of the certificate, either 'server' or 'client'.
        key_size (int): Size of the RSA key.
        validity_days (int): Number of days the certificate is valid.
        country (str): Country name for the certificate.
        state (str): State name for the certificate.
        org_name (str): Organization name for the certificate.
        passphrase (str): Passphrase for encrypting the private key.
        san_list (list): List of Subject Alternative Names (SANs) for the certificate.
    """

    def __init__(self,
        ca,
        cert_type="server",
        cert_name=None,
        key_size=2048,
        validity_days=365,
        country="US",
        state="Utah",
        org_name="pcc_data_engineering",
        passphrase=None,
        san_list=None):
        """
        Constructs all the necessary attributes for the ServerClientCertificate object.

        Args:
            ca (CertificateAuthority): An instance of the CertificateAuthority class.
            cert_type (str): Type of the certificate, either 'server' or 'client'.
            key_size (int): Size of the RSA key.
            validity_days (int): Number of days the certificate is valid.
            country (str): Country name for the certificate.
            state (str): State name for the certificate.
            org_name (str): Organization name for the certificate.
            passphrase (str): Passphrase for encrypting the private key.
            san_list (list): List of Subject Alternative Names (SANs) for the certificate.
        """
        self.ca = ca
        self.cert_type = cert_type
        self.cert_name = cert_name
        self.key_size = key_size
        self.validity_days = validity_days
        self.country = country
        self.state = state
        self.org_name = org_name
        self.passphrase = passphrase.encode() if passphrase else None
        self.san_list = san_list or []
        self.private_key = None # Private key for the server or client
        self.cert = None # Server or client certificate

    def _create_cert(self):
        """
        Creates the server or client certificate with the specified attributes.
        """
        subject = self._generate_subject(
            org_name=self.org_name,
            state=self.state,
            common_name=f"{self.org_name} {self.cert_type.capitalize()}",
            country=self.country
        )

        issuer = self.ca.ca_cert.subject  # CA is the issuer

        self.cert = self.create_and_sign_cert(
            subject=subject,
            issuer=issuer,
            private_key=self.ca.private_key,  # Signed by the CA's private key
            validity_days=self.validity_days,
            san_list=self.san_list
        )

    # Use the common save method
    def _save_cert_and_key(self, directory):
        self._save_to_directory(self.cert,
            self.private_key,
            directory,
            self.cert_name,
            self.passphrase)

    def generate_certificate(self, directory):
        """
        Generates the private key for the server or client 
        certificate and saves the certificate and key.
        """
        self.private_key = self.generate_rsa_key(self.key_size)
        self._create_cert()
        self._save_cert_and_key(directory)


# Assuming arguments will be passed via sys.argv
def main():
    ca_storage_path = sys.argv[1]  # Path passed from Ansible playbook
    passphrase = os.environ.get("CA_PASSPHRASE")

    # Load the CA if it exists
    if os.path.exists(ca_storage_path) and len(os.listdir(ca_storage_path)) > 0:
        try:
            ca = CertificateAuthority.from_file(ca_storage_path, passphrase)
            print(f"Loaded existing CA from {ca_storage_path}")
        except FileNotFoundError:
            print(f"CA files missing in {ca_storage_path}. Generating a new CA...")
            ca = CertificateAuthority(passphrase=passphrase)
            ca.generate_certificate_authority(ca_storage_path)
    else:
        # Use environment variables to set up CA attributes (passphrase, encryption type)
        encryption_type = os.environ.get("CA_ENCRYPTION_TYPE", "PKCS8")

        # Create the CA object
        ca = CertificateAuthority(
            key_size=4096,
            validity_years=10,
            country="US",
            state="Utah",
            org_name="pcc_data_engineering",
            passphrase=passphrase,
            encryption_type=encryption_type
        )
        ca.generate_certificate_authority(directory=ca_storage_path)

    # Check if we should generate a server/client certificate
    generate_certificate = os.environ.get("GENERATE_CERTIFICATE", "false").lower() == "true"

    if generate_certificate:
        # Generate server/client certificates based on environment variables
        cert_type = os.environ.get("CERT_TYPE", "server")
        cert_name = os.environ.get("CERT_NAME", f"{cert_type}_cert")
        validity_days = int(os.environ.get("VALIDITY_DAYS", 365))
        org_name = os.environ.get("ORG_NAME", "pcc_data_engineering")
        state = os.environ.get("STATE", "Utah")
        san_list = os.environ.get("SAN_LIST", "").split(',')

        cert = ServerClientCertificate(
            ca=ca,
            cert_type=cert_type,
            cert_name=cert_name,
            validity_days=validity_days,
            org_name=org_name,
            state=state,
            san_list=san_list
        )

        cert.generate_certificate(ca_storage_path)
    else:
        print("Skipping server/client certificate generation as per configuration.")

if __name__ == "__main__":
    main()
