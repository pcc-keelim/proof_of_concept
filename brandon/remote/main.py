import os
from datetime import datetime
from enum import Enum
import yaml

from fastapi import FastAPI

from brandon.remote.data_warehouse_remote import DataWarehouse
from smbclient import encrypted_drive


with open('secrets.yaml') as secrets:
    secrets = yaml.safe_load(secrets)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class QueryEngine(str, Enum):
    duckdb_query = 'duckdb'
    dask_query = 'dask'



@app.get("/submit_query/{query_engine}/{query_string}")
def execute_query(query_engine: QueryEngine, query_string: str):

    # Determine query engine
    if query_engine.value == 'duckdb':
        query_results_df = DataWarehouse.execute_query(query_string)
    elif query_engine.value == 'dask':
        pass

    # Determine file name and write to parquet
    run_time_stamp = str(datetime.now())[:-7].replace(" ","_").replace(":",'-')
    file_name = f"results_{run_time_stamp}.parquet"
    vm_query_results_filepath = os.path.join(DataWarehouse.VM_DEFAULT_QUERY_RESULTS_LOCATION, file_name)
    encrypted_query_results_filepath = os.path.join(DataWarehouse.ENCRYPTED_DEFAULT_QUERY_RESULTS_LOCATION, file_name)
    query_results_df.to_parquet(vm_query_results_filepath, index=False)

    # Write query results to encrypted drive
    x = encrypted_drive(
        username=secrets['encrypted_drive_credentials']['username'],
        password=secrets['encrypted_drive_credentials']['password']
    )
    x.upload_single_file(source_path=vm_query_results_filepath, destination_path=encrypted_query_results_filepath)

    # Prepend encrypted filepath with X:, since smbclient doesn't reference it
    encrypted_query_results_filepath = 'X:' + encrypted_query_results_filepath
    print(encrypted_query_results_filepath)


    return {"vm_query_results_filepath": vm_query_results_filepath, "encrypted_query_results_filepath": encrypted_query_results_filepath}