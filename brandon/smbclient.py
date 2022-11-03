import subprocess
from dataclasses import dataclass, field

@dataclass
class smbclient:
    """
    This class represents a generic smbclient connection.
        * Initializing the class does NOT open a steady connection that can be used with a context manager (e.g., 'with smbclient() as:').
        * Instead, the parameters it is supplied are stored, and the class methods can be used to issue one time commands to the smb server.
            * One time commands include things such as "get" (download) or "put" (upload)
        * If you were to instead connect to the smb server via terminal, you would be prompted to enter your password, and then would be given a CLI.
        * Thus, when using these class methods, you send a one-time parameterized request to the server instead of opening a session.
        * Proper usage would be initializing the class once to store credentials, and calling methods on the object as many times as needed.

    To add further functionality and convenience methods, please reference: https://www.samba.org/samba/docs/current/man-html/smbclient.1.html
    """
    server: str = None
    share: str = None
    domain: str = None
    smb_version: str = None
    username: str = None # windows login, should be firstname.lastname
    password: str = None # windows/vpn password
    base_command: str = field(init=False)

    def __post_init__(self):
        self.base_command = f"smbclient {self.server}/{self.share} -U {self.domain}/{self.username} -m {self.smb_version}"

    def download_single_file(self, source_path: str, destination_path: str) -> tuple:
        """
        Inputs:
            * source_path: absolute path to the file from the root of the smb server
            * destinaton_path: absolute path to the file from the root of your desired machine
        Output:
            * full_command: the full request issued to the server
            * stderror: the subprocess stderr (standard error)
            * stdout: the subprocess stdout (standard output)
        """
        option = '-c' # -c is command
        arg = f"'get \"{source_path}\" \"{destination_path}\"'" # get is upload
        full_command = self.base_command + ' ' + option + ' ' + arg
        response = subprocess.run(full_command, capture_output=True, text=True, shell=True, input=self.password)

        return (full_command, response.stderr, response.stdout)

    def download_multiple_files(self, source_path: str, destination_path: str, directory_pattern: str = "*", file_pattern: str = "*") -> tuple:
        """
        Inputs:
            * source_path: absolute path to the source directory from the root of the smb server
            * destinaton_path: absolute path to the destination directory from the root of your desired machine
            * directory_pattern: the pattern to identify desired directories within and below the source path
            * file_patten: the pattern to identify files within the desired directories
        Output:
            * full_command: the full request issued to the server
            * stderror: the subprocess stderr (standard error)
            * stdout: the subprocess stdout (standard output)
        """
        option = '-c' # -c is command
        arg = f"'prompt OFF;recurse ON;cd \"{source_path}\";lcd \"{destination_path}\";mask \"{file_pattern}\";mget \"{directory_pattern}\"'"
        full_command = self.base_command + ' ' + option + ' ' + arg
        response = subprocess.run(full_command, capture_output=True, text=True, shell=True, input=self.password)

        return (full_command, response.stderr, response.stdout)

    def upload_single_file(self, source_path: str, destination_path: str):
        """
        Inputs:
            * source_path: absolute path to the file from the root of your desired machine
            * destinaton_path: absolute path to the file from the root of the smb server
        Output:
            * full_command: the full request issued to the server
            * stderror: the subprocess stderr (standard error)
            * stdout: the subprocess stdout (standard output)
        """
        option = '-c' # -c is command
        arg = f"'put \"{source_path}\" \"{destination_path}\"'" # put is upload
        full_command = self.base_command + ' ' + option + ' ' + arg
        response = subprocess.run(full_command, capture_output=True, text=True, shell=True, input=self.password)

        return (full_command, response.stderr, response.stdout)

    def upload_multiple_files(self, source_path: str, destination_path: str, directory_pattern: str = "*", file_pattern: str = "*") -> tuple:
        """
        Inputs:
            * source_path: absolute path to the source directory from the root of the smb server
            * destinaton_path: absolute path to the destination directory from the root of your desired machine
            * directory_pattern: the pattern to identify desired directories within and below the source path
            * file_patten: the pattern to identify files within the desired directories
        Output:
            * full_command: the full request issued to the server
            * stderror: the subprocess stderr (standard error)
            * stdout: the subprocess stdout (standard output)
        """
        option = '-c' # -c is command
        arg = f"'prompt OFF;recurse ON;cd \"{destination_path}\";lcd \"{source_path}\";mask \"{file_pattern}\";mput \"{directory_pattern}\"'"
        full_command = self.base_command + ' ' + option + ' ' + arg
        response = subprocess.run(full_command, capture_output=True, text=True, shell=True, input=self.password)

        return (full_command, response.stderr, response.stdout)

@dataclass
class encrypted_drive(smbclient):
    """
    This is just a convenient subclass with default parameters to connect to the encrypted drive.
        * Paramaters supplied should be limited to username and password
    """
    server: str = '//encrypted.collectivemedicaltech.com'
    share: str = 'share'
    domain: str = 'CORP'
    smb_version: str = 'SMB3'

