SELECT *
FROM {{ source("gdb","patient_security_event") }}