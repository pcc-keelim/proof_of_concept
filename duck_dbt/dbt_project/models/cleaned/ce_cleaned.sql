SELECT
    id,
    facility_id,
    created_on,
    deleted_on,
    admit_date,
    discharge_date,
    type,
    patient_id
FROM {{ source('extracts', 'comprehensive_encounter') }}