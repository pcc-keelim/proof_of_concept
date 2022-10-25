{{
    config(
        materialized='incremental'
    )
}}

SELECT 
    "p_vd.id",
    "p_vd.attending_physician",
    "p_vd.chief_complaint",
    "p_vd.discharge_diagnosis",
    "p_vd.discharge_disposition_raw",
    "p_vd.last_seen",
    "p_vd.presumed_discharge_date"
FROM {{ source('parquet', 'patient_visit_details') }}

{%- if is_incremental() -%}
    
    WHERE "p_vd.id" NOT IN (SELECT "p_vd.id" FROM {{ this }})

{%- endif -%}