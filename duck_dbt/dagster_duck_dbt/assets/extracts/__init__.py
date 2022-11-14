from dagster import asset
import pandas as pd
from synthetic_data.DataGenClasses import FacilityDataClass, ComprehensiveEncounterDataClass, ComprehensiveEncounterMapDataClass


@asset
def facility() -> pd.DataFrame:
    """A table containing all facility information"""
    facility_list = []
    for facility_id in range(100):
        facility = FacilityDataClass(id=facility_id)
        facility_list.append(facility.__dict__)
    return pd.DataFrame.from_records(facility_list)


@asset
def comprehensive_encounter(facility:pd.DataFrame) -> pd.DataFrame:
    """A table containing all comprehensive encounter information"""
    ce_list = []
    for f_id in facility['id'].to_list():
        for ce_id in range(100):
            ce = ComprehensiveEncounterDataClass(
                facility_id=f_id
            )
            ce_list.append(ce.__dict__)
    return pd.DataFrame.from_records(ce_list)

@asset
def ce_visit_map(comprehensive_encounter:pd.DataFrame) -> pd.DataFrame:
    """A table containinng mappings from comprehensive encounters to patient visits"""
    ce_vm_list = []
    for ce_id in comprehensive_encounter['id'].to_list():
        for i in range(3):
            cevm = ComprehensiveEncounterMapDataClass(
                comprehensive_encounter_id=ce_id
            )
            ce_vm_list.append(cevm.__dict__)
    return pd.DataFrame.from_records(ce_vm_list)