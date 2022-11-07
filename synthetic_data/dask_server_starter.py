from dask.distributed import LocalCluster, Client
from dask_sql import Context, run_server
'''
This script does not currently execute properly. I have asked a question here to resolve 
https://dask.discourse.group/t/localcluster-runtimeerror-cannot-enter-context-context-object-at-is-already-entered/1264
'''

if __name__ == "__main__":
    cluster = LocalCluster(
        n_workers=2,
        memory_limit='3GiB',
    )

    print(cluster.dashboard_link)
    print(cluster.scheduler_address)

    local_client = Client(cluster)


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

    c = Context()
    print(c.DEFAULT_CATALOG_NAME)
    print(c.DEFAULT_SCHEMA_NAME)

    for table_name, path in data_locations.items():
        c.create_table(table_name=table_name,input_table=path)

    # c.run_server(client = local_client)
    run_server(context = c, client = local_client, )
    