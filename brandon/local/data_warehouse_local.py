from sshtunnel import SSHTunnelForwarder
import requests
import urllib.parse
import yaml
import pandas as pd
import time
import os
from pathlib import Path

class DataWarehouseLocal():
    """
    """
    __remote_host:str = 'rch-ds-analysis-01.int.collectivemedicaltech.com'
    __ssh_pkey:str = "~/.ssh/id_rsa"
    __remote_bind_address:str = '127.0.0.1'
    __remote_bind_port: int = 8000


    def __init__(self) -> None:
        cwd = Path(__file__).parent.resolve()
        with open(f'{cwd}/secrets.yaml') as secrets:
            self.__secrets = yaml.safe_load(secrets)

    def execute_query(self, query_engine: str, query_string: str) -> pd.DataFrame:
        """
        Submits a query to duckdb by:
            * establishing sshtunnel to vm running fastapi
            * passing query to fastapi
            * fastapi then submits query to duckdb
            * fast api stores query results at default locations on both vm and encrypted drive
            * query results filepaths returned here
        """
        # Prepare query for url insert
        query_string = urllib.parse.quote(query_string)

        with SSHTunnelForwarder(
            ssh_address_or_host=self.__remote_host,
            ssh_username=self.__secrets['ssh_credentials']['username'],
            ssh_password=self.__secrets['ssh_credentials']['password'],
            ssh_pkey=self.__ssh_pkey,
            ssh_private_key_password=self.__secrets['ssh_credentials']['key_password'],
            remote_bind_address=(self.__remote_bind_address,self.__remote_bind_port)
        )as server:
            response = requests.get(f'http://{self.__remote_bind_address}:{self.__remote_bind_port}/submit_query/{query_engine}/{query_string}').json()

        print(response)

        while not os.path.isfile(response['encrypted_query_results_filepath']):
            time.sleep(1)

        df = pd.read_parquet(response['encrypted_query_results_filepath'])
        return df
