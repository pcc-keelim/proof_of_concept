{{
    config(
        materialized='incremental'
    )
}}

SELECT  
    "p_v.id",
    "p_v.patient_id",
    "p_v.admit_date",
    "p_v.created_on",
    "p_v.account_number",
    "p_v.discharge_date",
    "p_v.data_source",
    "p_v.facility_id",
    "p_v.discharge_disposition",
    "p_v.visit_type",
    "p_v.major_class"

FROM {{ source('parquet', 'patient_visit') }}

{%- if is_incremental() -%}

    WHERE "p_v.id" NOT IN (SELECT "p_v.id" FROM {{ this }})

{%- endif -%}