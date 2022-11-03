import duckdb
import pandas as pd
import os

class DataWarehouse():
    """
    This class wraps duckdb and allows for:
        * initialization of the database if it does not already exist
        * execution of queries if it does already exist
    """

    DUCKDB_FILE_LOCATION = '/data/DataWarehouse.duckdb'
    VM_DEFAULT_QUERY_RESULTS_LOCATION = '/data/temp/query_results'
    ENCRYPTED_DEFAULT_QUERY_RESULTS_LOCATION = '/data/temp/query_results'

    def __init__(self) -> None:
        """
        Initialize duckdb and get secrets
        """
        if not os.path.isfile(DataWarehouse.DUCKDB_FILE_LOCATION):
            DataWarehouse.__init_duckdb()

    @staticmethod
    def __init_duckdb() -> None:
        """
        """
        # Establish the duckdb file
        con = duckdb.connect(database=DataWarehouse.DUCKDB_FILE_LOCATION, read_only=False)
        # Create all necessary tables
        DataWarehouse.__create_tables(con)

    @staticmethod
    def __create_tables(con:duckdb.DuckDBPyConnection) -> None:
        """
        Creates views for all data sources in /data/00_extract/
        """
        # Get all directories in /data/00_extract/ for which parquet files exists
        table_dirs = []
        for root, dirs, files in os.walk('/data/00_extract/', topdown=False):
            for dir in dirs:
                parquet_files_in_dir = [x for x in os.listdir(os.path.join(root, dir)) if '.parquet' in x]
                if parquet_files_in_dir:
                    table_dirs.append(os.path.join(root, dir))
        print(table_dirs)

        # Create views for each of the data sources
        for table_dir in table_dirs:
            table_name = table_dir.replace('/data/00_extract/', '').replace('/', '_')
            con.execute(f"CREATE VIEW {table_name} AS SELECT * FROM '{table_dir}/*.parquet'")

    @staticmethod
    def execute_query(query_string:str) -> pd.DataFrame:
        """
        """
        con = duckdb.connect(database=DataWarehouse.DUCKDB_FILE_LOCATION, read_only=True)
        results: list = con.execute(query_string).df()
        return results