from dagster_dbt import DbtCliResource

from typo.records.assets.constants import DBT_DIRECTORY


class DbtResource(DbtCliResource):
    def __init__(self, **kwargs):
        super().__init__(project_dir=DBT_DIRECTORY, **kwargs)
