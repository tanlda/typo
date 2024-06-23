from dagster import Config
from typing import Optional


class RecordsConfig(Config):
    key: str
    date: str
    user_id: str
    partition: str
    timestamp: str
    shuffle_rows: Optional[bool] = True
    deduplicate_rows: Optional[bool] = True
    store_user_id: Optional[bool] = True
