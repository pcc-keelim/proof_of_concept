{{ config(tags="external") }}

SELECT "f.id",
    "f.name",
    "f.address",
    "f.phone",
    "f.participating",
    "f.city",
    "f.state",
    "f.zip",
    "f.created_on"
FROM {{ source('parquet', 'facility')}}