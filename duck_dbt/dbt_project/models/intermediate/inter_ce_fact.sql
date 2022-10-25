{{
    config(
        materialized='incremental'
    )
}}

SELECT
    ce.*,
    cevm.*
FROM {{ ref("stg_comprehensive_encounter") }} ce
    LEFT JOIN {{ ref("stg_ce_visit_map") }} cevm ON ce."ce.id" = cevm."cevm.comprehensive_encounter_id"

{%- if is_incremental() -%}

    WHERE ce."ce.id" NOT IN (SELECT "ce.id" FROM {{ this }})
    
{%- endif -%}