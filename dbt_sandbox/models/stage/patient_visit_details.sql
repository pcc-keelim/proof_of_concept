SELECT *
FROM {{ source("gdb","patient_visit_details") }}