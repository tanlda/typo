from dagster import AssetExecutionContext
from dagster_dbt import (
    dbt_assets,
    DbtCliResource,
    DagsterDbtTranslator,
)

from typo.shared.constants import DBT_DIRECTORY

dbt_manifest_path = DBT_DIRECTORY / "target" / "manifest.json"


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    pass


@dbt_assets(
    manifest=dbt_manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
    exclude="tag:exclude"
)
def dbt_dashes(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()
