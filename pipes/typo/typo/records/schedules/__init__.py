from dagster_dbt import build_schedule_from_dbt_selection

from typo.records.assets.dashes import dbt_dashes

hourly_dbt_assets_schedule = build_schedule_from_dbt_selection(
    dbt_assets=[dbt_dashes],
    job_name="hourly_dbt_models",
    cron_schedule="0 * * * *",
    dbt_select="tag:hourly",
)
