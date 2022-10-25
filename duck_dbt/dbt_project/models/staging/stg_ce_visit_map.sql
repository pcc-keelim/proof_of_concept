{{
    config(
        materialized='incremental'
    )
}}

SELECT
    "cevm.id",
    "cevm.comprehensive_encounter_id",
    "cevm.patient_visit_id",
    "cevm.deleted_on",
    "cevm.created_on",
    "cevm.patient_id",
    "cevm.is_sensitive"
FROM {{ source('parquet', 'ce_visit_map') }}

{%- if is_incremental() -%}

    WHERE "cevm.id" NOT IN (SELECT "cevm.id" FROM {{ this }})

{%- endif -%}