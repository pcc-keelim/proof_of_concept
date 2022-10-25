{{ 
    config(
        materialized='incremental'
    ) 
}}

SELECT 
    "ce.id",
    "ce.facility_id",
    "ce.created_on",
    "ce.deleted_on",
    "ce.matching_method",
    "ce.matching_method_identifier",
    "ce.admit_date",
    "ce.discharge_date",
    "ce.type",
    "ce.patient_id"
FROM {{ source('parquet', 'comprehensive_encounter') }}

{%- if is_incremental() -%}

    WHERE "ce.created_on" >= (SELECT MAX("ce.created_on") FROM {{ this }})

{%- endif -%}