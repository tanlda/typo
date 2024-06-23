import os
from dagster import Definitions, load_assets_from_modules

from typo.records.assets import records, dashes
from typo.records.sensors import storage_records_sensor
from typo.records.jobs import lakehouse_records_job, warehouse_records_job
from typo.records.schedules import hourly_dbt_assets_schedule

from typo.shared.resources import (
    StorageResource,
    WarehouseResource,
    LakehouseResource,
    IcebergResource,
    DbtResource,
)

all_assets = [
    *load_assets_from_modules([dashes], group_name="dashes"),
    *load_assets_from_modules([records], group_name="records"),
]

all_jobs = [
    lakehouse_records_job,
    warehouse_records_job,
]

all_schedules = [
    hourly_dbt_assets_schedule,
]

all_sensors = [
    storage_records_sensor,
]

defs = Definitions(
    assets=all_assets,
    sensors=all_sensors,
    schedules=all_schedules,
    jobs=all_jobs,
    resources={
        "storage": StorageResource(
            bucket_name=os.environ.get("AWS_BUCKET_NAME", default="microtypo-prod-bucket"),
            region_name=os.environ.get("AWS_REGION_NAME", default="ap-southeast-1"),
        ),
        "warehouse": WarehouseResource(
            username=os.environ.get("DB_USERNAME", default="app"),
            database=os.environ.get("DB_DATABASE", default="app"),
            password=os.environ.get("DB_PASSWORD", default="password"),
            host=os.environ.get("DB_HOST", default="warehouse.io"),
            port=os.environ.get("DB_PORT", default=5432),
        ),
        "lakehouse": LakehouseResource(
            region_name="ap-southeast-1",
            endpoint="lakehouse.io",
            bucket_name="microtypo",
            access_key="admin",
            secret_key="password",
        ),
        "iceberg": IcebergResource(
            uri="iceberg.io",
            access_key="admin",
            secret_key="password",
            endpoint="lakehouse.io",
        ),
        "dbt": DbtResource()
    }
)
