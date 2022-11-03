import os
from typing import Union
import duckdb
import pandas as pd
from dagster import Field, PartitionKeyRange, _check as check, io_manager, IOManager, OutputContext, InputContext
from dagster._seven.temp_dir import get_system_temp_directory
from .parquet_io_manager import ParquetIOManager


class DuckDBParquetIOManager(ParquetIOManager):
    """Stores data in parquet files and created duckdb views over those files."""

    def handle_output(self, context: OutputContext, obj: Union[pd.DataFrame, None]) -> None:
        if obj is not None:
            super().handle_output(context, obj)
            con = self._connect_duckdb(context)
            path = self._get_path(context)
            if context.has_asset_partitions:
                to_scan = os.path.join(os.path.dirname(path), "*.parquet")
            else:
                to_scan = path
            con.execute(f"CREATE SCHEMA IF NOT EXISTS {self._schema(context)};")
            con.execute(f"CREATE OR REPLACE VIEW {self._table_path(context)} as ( SELECT * FROM parquet_scan('{to_scan}'));")
        else:
            con = self._connect_duckdb(context)
            path = self._get_path(context)
            if context.has_asset_partitions:
                start, end = context.asset_partitions_time_window()
                con.execute(f"COPY (SELECT * FROM {self._table_path(context)}) TO '{path}.parquet' (FORMAT PARQUET)")
            else:
                con.execute(f"COPY {self._table_path(context)} TO '{path}' (FORMAT PARQUET)")
    
    def load_input(self, context: InputContext) -> Union[pd.DataFrame, str]:
        check.invariant(
            not context.has_asset_partitions
            or context.asset_partition_key_range == PartitionKeyRange(
                context.asset_partitions_def.get_first_partition_key(),
                context.asset_partitions_def.get_last_partition_key(),
            ),
            "Loading a subselection of partitions is not yet supported",
        )       
        if context.dagster_type.typing_type == pd.DataFrame:
            con = self._connect_duckdb(context)
            return con.execute(f"SELECT * FROM {self._table_path(context)}").fetch_df()

        check.failed(
            f"Inputs of type {context.dagster_type} not supported. Please specify a valid type" 
            "for this input either on the argument of the @asset-decorated function."
        )

    def _connect_duckdb(self, context: Union[OutputContext, InputContext]) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(database=context.resource_config["duckdb_path"], read_only=False)

    def _schema(self, context: Union[OutputContext, InputContext]) -> str:
        return f"{context.asset_key.path[-2]}"
    
    def _table_path(self, context: Union[OutputContext, InputContext]) -> str:
        return f"{self._schema(context)}.{context.asset_key.path[-1]}"


@io_manager(
    config_schema={"base_path": Field(str, is_required=False), "duckdb_path": str},
)
def duckdb_parquet_io_manager(init_context):
    return DuckDBParquetIOManager(
        base_path=init_context.resource_config.get("base_path", "/Users/carlss/repos/.sandbox/data")
    )