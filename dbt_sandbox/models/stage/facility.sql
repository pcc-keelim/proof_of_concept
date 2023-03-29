SELECT *
FROM {{ source("gdb","facility") }}
WHERE participating = 1
  AND id != '1'