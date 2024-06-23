import polars as pl

from typo.shared.resources import StorageResource
from typo.records.configs import RecordsConfig


def download_records_util(storage: StorageResource, config: RecordsConfig):
    client = storage.get_client()

    response = client.get_object(Bucket=storage.bucket_name, Key=config.key)
    df = pl.read_csv(response["Body"].read())

    if config.deduplicate_rows:
        df = df.unique(subset=["hostname", "timestamp"]).sort(by="timestamp")

    if config.shuffle_rows:
        df = df.with_columns(pl.col("timestamp").shuffle())

    if config.store_user_id:
        columns = df.columns
        df = df.with_columns(user_id=pl.lit(config.user_id))
        df = df[["user_id"] + columns]

    return df
