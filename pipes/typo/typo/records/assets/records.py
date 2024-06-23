import tempfile
import polars as pl
from dagster import asset
from dagster import (
    AssetKey,
    MetadataValue,
    MaterializeResult,
    AssetExecutionContext,
)

from typo.records.configs import RecordsConfig
from typo.records.utils import download_records_util
from typo.shared.resources import StorageResource, LakehouseResource, WarehouseResource
from typo.shared.utils import Timer


@asset(
    deps=[],
    compute_kind="Python",
)
def warehouse_records(
        context: AssetExecutionContext,
        warehouse: WarehouseResource,
        storage: StorageResource,
        config: RecordsConfig,
):
    """
        Records SQL [storage -> warehouse.io]
    """
    with Timer() as download:
        added = download_records_util(storage=storage, config=config)
        added = added.with_columns(pl.col("timestamp").str.to_datetime())

    with Timer() as append:
        added.write_database(
            table_name="records",
            connection=warehouse.get_connection(),
            if_table_exists="append",
            engine="sqlalchemy",
        )

    return MaterializeResult(
        asset_key=AssetKey("warehouse_records"),
        metadata={
            "len": MetadataValue.int(len(added)),
            "key": MetadataValue.text(config.key),
            "date": MetadataValue.text(str(config.date)),
            "download (elapsed)": MetadataValue.float(download.elapsed),
            "append (elapsed)": MetadataValue.float(append.elapsed),
        },
    )


@asset(
    deps=[],
    compute_kind="Python",
)
def lakehouse_records(
        context: AssetExecutionContext,
        lakehouse: LakehouseResource,
        storage: StorageResource,
        config: RecordsConfig,
):
    """
        Records .parquet [storage -> lakehouse.io]
    """

    with Timer() as download:
        added = download_records_util(storage=storage, config=config)
        added = added.with_columns(pl.col("timestamp").str.to_datetime())

    with Timer() as replace, tempfile.NamedTemporaryFile() as tmpfile:
        client = lakehouse.get_client()
        parquet_file = f"records/{config.user_id}/records.{config.date}.parquet"
        try:
            exist = pl.read_parquet(
                source=f"s3://{lakehouse.bucket_name}/{parquet_file}",
                storage_options=lakehouse.get_storage_options(),
            )
        except pl.ComputeError:
            exist = pl.DataFrame()
        finally:
            exist = pl.concat([exist, added])
            exist.write_parquet(tmpfile.name)
            client.fput_object(lakehouse.bucket_name, parquet_file, tmpfile.name)

    return MaterializeResult(
        asset_key=AssetKey("lakehouse_records"),
        metadata={
            "len": MetadataValue.int(len(added)),
            "key": MetadataValue.text(config.key),
            "date": MetadataValue.text(str(config.date)),
            "download (elapsed)": MetadataValue.float(download.elapsed),
            "replace (elapsed)": MetadataValue.float(replace.elapsed),
        },
    )
