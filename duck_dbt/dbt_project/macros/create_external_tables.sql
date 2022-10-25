{% macro create_external_tables(select=none) %}
    
    {%- set source_nodes = graph.sources.values() if graph.sources else [] -%}
    
    {%- if source_nodes|length == 0 -%}
        {%- do log('No external sources selected', info = true) -%}
    {%- endif -%}

    {%- for node in source_nodes -%}
        {%- if node.external -%}
            {%- set external = node.external -%}

            CREATE SCHEMA IF NOT EXISTS {{node.source_name}};
            CREATE OR REPLACE VIEW {{source(node.source_name, node.name).include(database=False)}} AS 
            (
                SELECT * FROM '{{external.location}}'
            );
        {%- endif -%}
    {%- endfor -%}
{% endmacro %}