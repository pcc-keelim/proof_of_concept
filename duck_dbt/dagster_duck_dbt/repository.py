import os
from dagster import (
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
    repository,
    with_resources
)
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource
from dagster_duckdb import build_duckdb_io_manager
from dagster_duckdb_pandas import DuckDBPandasTypeHandler
from duck_dbt.dagster_duck_dbt.assets import extracts
from duck_dbt.dagster_duck_dbt.resources import duckdb_parquet_io_manager

DBT_PROJECT_DIR = os.path.join(os.path.dirname(__file__), "../dbt_project")
DBT_PROFILES_DIR = os.path.join(os.path.dirname(__file__), "../dbt_project/config")

extract_assets = load_assets_from_package_module(
    extracts,
    group_name="extracts",
    # Tells dagster to put extracts in extract schema in duckdb
    key_prefix=["duckdb", "extracts"]
)

dbt_assets = load_assets_from_dbt_project(
    DBT_PROJECT_DIR,
    DBT_PROFILES_DIR,
    key_prefix=["duckdb", "dbt_schema"],
    source_key_prefix=["duckdb"]
)


daily_job = define_asset_job("daily_job", selection="*")

@repository
def dagster_duck_dbt():
    #duckdb_io_manager = build_duckdb_io_manager(type_handlers=[DuckDBPandasTypeHandler()])
    duckdb_io_manager = duckdb_parquet_io_manager
    return with_resources(
        extract_assets + dbt_assets,
        resource_defs={
            "io_manager": duckdb_io_manager.configured(
                {"duckdb_path": os.path.join(DBT_PROJECT_DIR, "warehouse.duckdb")}
            ),
            "dbt": dbt_cli_resource.configured(
                {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
            ),
        },
    ) + [ScheduleDefinition(job=daily_job, cron_schedule="@daily"),]