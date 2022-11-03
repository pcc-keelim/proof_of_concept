SELECT *
FROM {{
    metrics.calculate(
        metric('visit_count'),
        grain='day',
        dimensions=['facility_id', 'type']
    )
}}