SELECT 
    ce_main.facility_id, 
    ce_main.type, 
    ce_main.admit_date, 
    ce_main.count,
    f.name
FROM (
SELECT 
    facility_id, 
    type, 
    datetrunc('month',admit_date) AS admit_date, 
    count(id) as count
FROM {{ ref('ce') }} 
GROUP BY facility_id, type, datetrunc('month',admit_date)
) ce_main
LEFT JOIN {{ ref('facility') }} f on f.id=ce_main.facility_id