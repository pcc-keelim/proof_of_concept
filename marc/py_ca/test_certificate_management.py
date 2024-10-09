import os
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

from certificate_management import CertificateAuthority, ServerClientCertificate


class TestCertificateManagement(unittest.TestCase):

    def setUp(self):
        """
        Set up a temporary directory for storing generated certificates and keys.
        """
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Clean up by removing the temporary directory and all its contents.
        """
        shutil.rmtree(self.test_dir)

    def test_create_certificate_authority(self):
        """
        Test the generation of a Certificate Authority (CA) 
        and ensure the certificate and key are saved correctly.
        """
        ca = CertificateAuthority(
            key_size=2048,  # Smaller key size for faster test execution
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )

        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        ca_cert_path = os.path.join(self.test_dir, 'ca', 'ca.cert.pem')
        ca_key_path = os.path.join(self.test_dir, 'ca', 'ca.key.pem')

        # Check that the certificate and key files were created
        self.assertTrue(os.path.exists(ca_cert_path))
        self.assertTrue(os.path.exists(ca_key_path))

        # Load the certificate and ensure it is a valid x509 certificate
        with open(ca_cert_path, 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())

        self.assertIsInstance(ca_cert, x509.Certificate)

    def test_create_server_certificate_with_validation(self):
        """
        Test the generation of a server certificate signed 
        by the CA and validate it against the CA certificate.
        """
        # First, create the Certificate Authority (CA)
        ca = CertificateAuthority(
            key_size=2048,  # Smaller key size for faster test execution
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        # Now create the server certificate
        cert_name = "server_test_cert"
        server_cert = ServerClientCertificate(
            ca=ca,
            cert_type="server",
            cert_name=cert_name,
            key_size=2048,
            validity_days=365,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            san_list=["example.com"]
        )

        server_cert.generate_certificate(self.test_dir)

        server_cert_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.cert.pem')
        server_key_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.key.pem')

        # Check that the server certificate and key files were created
        self.assertTrue(os.path.exists(server_cert_path))
        self.assertTrue(os.path.exists(server_key_path))

        # Load the server certificate and ensure it is a valid x509 certificate
        with open(server_cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())
        self.assertIsInstance(cert, x509.Certificate)

        # Validate that the server certificate is signed by the CA
        with open(os.path.join(self.test_dir, 'ca', 'ca.cert.pem'), 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())

        ca_public_key = ca_cert.public_key()

        # Ensure that the server certificate was signed by the CA's private key
        try:
            ca_public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        except Exception as e:
            self.fail(f"Server certificate validation against CA failed: {str(e)}")

        # If no exception was raised, the signature is valid
        print("Server certificate successfully validated against CA.")

    def test_skip_certificate_generation(self):
        """
        Test skipping server/client certificate generation.
        """
        # Set up a CA
        ca = CertificateAuthority(
            key_size=2048,  # Smaller key size for faster test execution
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        cert_name = "server_test_cert"

        # Do not call `generate_certificate`, and ensure no certificate is created
        server_cert_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.cert.pem')
        server_key_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.key.pem')

        # Check that the server certificate and key files do not exist
        self.assertFalse(os.path.exists(server_cert_path))
        self.assertFalse(os.path.exists(server_key_path))

    def test_create_certificate_authority_with_different_key_size(self):
        """
        Test the generation of a Certificate Authority with a 4096-bit RSA key.
        """
        ca = CertificateAuthority(
            key_size=4096,  # Larger key size for this test
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        ca_cert_path = os.path.join(self.test_dir, 'ca', 'ca.cert.pem')
        ca_key_path = os.path.join(self.test_dir, 'ca', 'ca.key.pem')

        # Check that the certificate and key files were created
        self.assertTrue(os.path.exists(ca_cert_path))
        self.assertTrue(os.path.exists(ca_key_path))

        # Load the private key to check its size
        with open(ca_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=b"testpassphrase")
        self.assertEqual(private_key.key_size, 4096)

    def test_create_client_certificate(self):
        """
        Test the generation of a client certificate signed by the CA.
        """
        # First, create the Certificate Authority (CA)
        ca = CertificateAuthority(
            key_size=2048,
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        # Now create the client certificate
        cert_name = "client_test_cert"
        client_cert = ServerClientCertificate(
            ca=ca,
            cert_type="client",
            cert_name=cert_name,
            key_size=2048,
            validity_days=365,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            san_list=["client.example.com"]
        )

        client_cert.generate_certificate(self.test_dir)

        client_cert_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.cert.pem')
        client_key_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.key.pem')

        # Check that the client certificate and key files were created
        self.assertTrue(os.path.exists(client_cert_path))
        self.assertTrue(os.path.exists(client_key_path))

        # Load the client certificate and ensure it is valid
        with open(client_cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())
        self.assertIsInstance(cert, x509.Certificate)


    def test_private_key_encryption_with_passphrase(self):
        """
        Test that the private key is encrypted with the provided passphrase.
        """
        ca = CertificateAuthority(
            key_size=2048,
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        ca_key_path = os.path.join(self.test_dir, 'ca', 'ca.key.pem')

        # Attempt to load the private key without the passphrase (should fail)
        with open(ca_key_path, 'rb') as f:
            with self.assertRaises(TypeError):  # TypeError raised when passphrase is missing
                serialization.load_pem_private_key(f.read(), password=None)

        # Now load the private key with the correct passphrase
        with open(ca_key_path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=b"testpassphrase")
        self.assertIsInstance(private_key, rsa.RSAPrivateKey)

    def test_san_in_server_certificate(self):
        """
        Test that Subject Alternative Names (SANs) are correctly included in the server certificate.
        """
        # First, create the Certificate Authority (CA)
        ca = CertificateAuthority(
            key_size=2048,
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        # Now create the server certificate with SANs
        cert_name = "server_test_cert_with_san"
        server_cert = ServerClientCertificate(
            ca=ca,
            cert_type="server",
            cert_name=cert_name,
            key_size=2048,
            validity_days=365,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            san_list=["example.com", "www.example.com"]
        )

        server_cert.generate_certificate(self.test_dir)

        server_cert_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.cert.pem')

        # Load the server certificate and ensure it has the SAN extension
        with open(server_cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())

        san_extension = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        self.assertEqual(
            san_extension.value.get_values_for_type(x509.DNSName),
            ["example.com", "www.example.com"])

    def test_certificate_validity_period(self):
        """
        Test that the validity period is correctly set in the generated certificates.
        """
        # First, create the Certificate Authority (CA)
        ca = CertificateAuthority(
            key_size=2048,
            validity_years=5,  # Test with a custom validity period
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        ca_cert_path = os.path.join(self.test_dir, 'ca', 'ca.cert.pem')

        # Load the CA certificate and check the validity period
        with open(ca_cert_path, 'rb') as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())

        expected_not_after = datetime.utcnow() + timedelta(days=365 * 5)
        self.assertAlmostEqual(ca_cert.not_valid_after, expected_not_after, delta=timedelta(days=1))

        # Now create a server certificate with a 1-year validity period
        cert_name = "server_test_cert_validity"
        server_cert = ServerClientCertificate(
            ca=ca,
            cert_type="server",
            cert_name=cert_name,
            key_size=2048,
            validity_days=365,  # 1 year
            country="US",
            state="Utah",
            org_name="TestOrganization",
            san_list=["example.com"]
        )
        server_cert.generate_certificate(self.test_dir)

        server_cert_path = os.path.join(self.test_dir, cert_name, f'{cert_name}.cert.pem')

        # Load the server certificate and check the validity period
        with open(server_cert_path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())

        expected_not_after_server = datetime.utcnow() + timedelta(days=365)
        self.assertAlmostEqual(
            cert.not_valid_after,
            expected_not_after_server,
            delta=timedelta(days=1))

    def test_load_certificate_authority_from_file(self):
        """
        Test loading a Certificate Authority (CA) from disk.
        """
        ca = CertificateAuthority(
            key_size=2048,
            validity_years=1,
            country="US",
            state="Utah",
            org_name="TestOrganization",
            passphrase="testpassphrase"
        )
        ca.generate_certificate_authority(directory=self.test_dir, key_path=self.test_dir)

        # Load the CA from the saved files
        loaded_ca = CertificateAuthority.from_file(
            directory=os.path.join(self.test_dir, 'ca'),
            passphrase="testpassphrase")

        # Ensure the loaded CA has the correct attributes
        self.assertIsInstance(loaded_ca.ca_cert, x509.Certificate)
        self.assertIsInstance(loaded_ca.private_key, rsa.RSAPrivateKey)


if __name__ == '__main__':
    unittest.main()
