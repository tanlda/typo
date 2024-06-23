from dagster import define_asset_job

lakehouse_records_job = define_asset_job(
    name="lakehouse_records_job",
    selection="lakehouse_records",
)

warehouse_records_job = define_asset_job(
    name="warehouse_records_job",
    selection="warehouse_records",
)
