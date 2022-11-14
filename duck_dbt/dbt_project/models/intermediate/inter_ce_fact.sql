SELECT
    ce.id as id,
    ce.facility_id as facility_id,
    ce.created_on as created_on,
    ce.deleted_on as deleted_on,
    ce.admit_date as admit_date,
    ce.discharge_date as discharge_date,
    ce.type as type,
    ce.patient_id as patient_id,
    cevm.id as cevm_id,
    cevm.comprehensive_encounter_id as comprehensive_encounter_id,
    cevm.patient_visit_id as patient_visit_id,
    cevm.deleted_on as cevm_deleted_on,
    cevm.created_on as cevm_created_on,
    cevm.patient_id as cevm_patient_id,
    cevm.is_sensitive as is_sensitive
FROM {{ ref("ce_cleaned") }} ce
    LEFT JOIN {{ ref("ce_visit_map_cleaned") }} cevm 
        ON ce.id = cevm.comprehensive_encounter_id