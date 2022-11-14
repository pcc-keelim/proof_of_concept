import os
from typing import Union
import pandas as pd
from dagster import Field, IOManager, InputContext, OutputContext, _check as check, io_manager
from dagster._seven.temp_dir import get_system_temp_directory


class ParquetIOManager(IOManager):
    """
    This IOManager will take in a pandas dataframe or dbt table and store it in parqeut at the specified path.

    It stores outputs for different partitions in different filepaths.

    Downstream ops can either load this dataframe or simply retrieve a path to where the data is stored.
    """

    def __init__(self, base_path) -> None:
        self._base_path = base_path

    def _get_path(self, context: Union[InputContext, OutputContext]):
        key = context.asset_key.path[-1]

        if context.has_asset_partitions:
            start, end = context.asset_partitions_time_window
            dt_format = "%Y%m%d%H%M%S"
            partition_str = start.strftime(dt_format) + "_" + end.strftime(dt_format)
            return os.path.join(self._base_path, key, f"{partition_str}.parquet")
        else:
            return os.path.join(self._base_path, f"{key}.parquet")

    def handle_output(
            self, 
            context: OutputContext, 
            obj: pd.DataFrame
        ) -> None:
        path = self._get_path(context)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if isinstance(obj, pd.DataFrame):
            row_count = len(obj)
            context.log.info(f"Row Count: {row_count}")
            obj.to_parquet(path=path, index=False)
        else:
            raise Exception(f"Outpus of type {type(obj)} not supported.")
        
        context.add_output_metadata({"row_count": row_count, "path": path})
        

    def load_input(self, context: InputContext) -> Union[pd.DataFrame, str]:
        path = self._get_path(context)
        if context.dagster_type.typing_type == pd.DataFrame:
            return pd.read_parquet(path)
        
        return check.failed(
            f"Inputs of type {context.dagster_type} not supported. Please specify a valid type"
            "for this input either on the argument of the @asset-decorated function."
        )


@io_manager(
    config_schema={"base_path": Field(str, is_required=False)},
)
def local_parquet_io_manager(init_context):
    return ParquetIOManager(
        base_path=init_context.resource_config.get("base_path", "/Users/carlss/repos/.sandbox/data")
    )
