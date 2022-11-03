SELECT
    id,
    name,
    state,
    join_date
FROM {{ source('extracts', 'facility') }}