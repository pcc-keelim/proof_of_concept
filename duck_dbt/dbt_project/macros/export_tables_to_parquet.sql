{% macro export_tables_to_parquet(select=none) %}
    {%- if execute -%}
        {%- set model_nodes = graph.nodes.values() | selectattr("resource_type", "equalto", "model") if graph.nodes else [] -%}

        {%- for model in model_nodes -%}

            {%- if  model.config.meta.to_parquet -%}

                COPY {{model.schema}}.{{model.name}} to './{{model.name}}.parquet' (FORMAT PARQUET) ;

            {%- endif -%}

        {%- endfor -%}

    {%- endif -%}

{% endmacro %}

