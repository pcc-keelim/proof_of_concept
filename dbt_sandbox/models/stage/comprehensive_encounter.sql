SELECT *
FROM {{ source("gdb","comprehensive_encounter") }}
where deleted_on is null