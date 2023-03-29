SELECT *
FROM {{ ref('comprehensive_encounter') }} ce
LEFT JOIN {{ ref('comprehensive_encounter_visit_map') }} cevm 
    ON ce.id = cevm.comprehensive_encounter_id
LEFT JOIN {{ ref('patient_visit') }} pv
    ON cevm.patient_visit_id = pv.id
LEFT JOIN {{ ref('patient_visit_details') }} pvd
    ON pvd.id = pv.id