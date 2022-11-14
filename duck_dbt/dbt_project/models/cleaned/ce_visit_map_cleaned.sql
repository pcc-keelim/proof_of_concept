SELECT
    id,
    comprehensive_encounter_id,
    patient_visit_id,
    deleted_on,
    created_on,
    patient_id,
    is_sensitive
FROM {{ source( 'extracts', 'ce_visit_map' ) }}