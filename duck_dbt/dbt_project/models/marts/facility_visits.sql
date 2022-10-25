SELECT *
FROM {{
  met  rics.calculate(
        metric('visit_count'),
        grain='day',
        dimensions=['ce.facility_id', 'p_v.major_class']
    )
}}