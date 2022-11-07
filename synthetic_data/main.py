from os import path
from datetime import datetime
from fastapi import FastAPI
from dask.distributed import LocalCluster, Client
from dask_sql import Context, run_server
import duckdb

data_locations = {
    # "table_name":"location",
    "facility":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/facility.parquet",
    "comprehensive_encounter":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/comprehensive_encounter.parquet",
    "patient_visit":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/patient_visit.parquet",
    "comprehensive_encounter_map":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/comprehensive_encounter_map.parquet",
    "patient_diagnosis":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/patient_diagnosis.parquet",
    "patient_visit_pds_care_provider":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/patient_visit_pds_care_provider.parquet",
    "patient_visit_details":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/patient_visit_details.parquet",
    "PatientLanguage":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/PatientLanguage.parquet",
    "PatientDisability":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/PatientDisability.parquet",
    "PatientMarital":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/PatientMarital.parquet",
    "PatientRace":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/PatientRace.parquet",
    "PatientEthnicity":"C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data/PatientEthnicity.parquet",
}

def create_dask_sql_cluster(data_locations:dict):
    # This commented out code is a future state
    # We would like to have a stable cluster but not able to set up at this time. 
    # cluster = LocalCluster(
    #     n_workers=5,
    #     memory_limit="2Gib",
    # )
    # client = Client(cluster)
    # my_scheduler_address = cluster.scheduler_address
    # print(f"my_scheduler_address = {my_scheduler_address}")
    # print(f"cluster.dashboard_link = {cluster.dashboard_link}")
    c = Context()
    print(c.DEFAULT_CATALOG_NAME)
    print(c.DEFAULT_SCHEMA_NAME)

    for table_name, path in data_locations.items():
        c.create_table(table_name=table_name,input_table=path)
    return c
local_client = Client()
c = create_dask_sql_cluster(data_locations=data_locations)

def create_duckdb(data_locations):
    with duckdb.connect("database.duckdb") as con:
        for table,path in data_locations.items():
            sql = f"CREATE VIEW {table} AS SELECT * FROM parquet_scan('{path}')"
            con.execute(sql)

create_duckdb(data_locations=data_locations)

app = FastAPI()
default_storage_location = "C:/Users/marc.keeling/Development/.sandbox/proof_of_concept/synthetic_data/data"

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/submit_dask_query/{query_string}/{output_path}")
def execute_dask_query(query_string,output_path):
    ### This section is commented out. Need to get stable dask-sql-server up and running
    # with create_engine('presto://localhost:8080/hive/default').connect() as connection:
    #     results = read_sql_query(query_string, con=connection)

    results = c.sql(query_string).compute()
        
    run_time_stamp = str(datetime.now())[:-7].replace(" ","_").replace(":",'-')
    file_name = f"results_{run_time_stamp}.parquet"
    full_file_path = path.join(default_storage_location, file_name)
    results.to_parquet(full_file_path)

    return {"Success": f"'{full_file_path}' created."}

@app.get("/submit_duckdb_query/{query_string}/{output_path}")
def execute_duckdb_query(query_string,output_path):
    duckdb_path = "./database.duckdb"
    with duckdb.connect(duckdb_path) as con:
        results = con.execute(query_string).df()
    
    run_time_stamp = str(datetime.now())[:-7].replace(" ","_").replace(":",'-')
    file_name = f"results_{run_time_stamp}.parquet"
    full_file_path = path.join(default_storage_location, file_name)
    results.to_parquet(full_file_path)

    return {"Success": f"'{full_file_path}' created."}