from typing import Optional

from minio import Minio
from dagster_aws.s3 import S3Resource
from dagster import ConfigurableResource
from dagster_dbt import DbtCliResource
from pyiceberg.catalog import Catalog, load_catalog

from typo.shared.constants import DBT_DIRECTORY


class StorageResource(S3Resource):
    bucket_name: str


class WarehouseResource(ConfigurableResource):
    host: str
    database: str
    username: str
    password: str
    port: int = 5432

    def get_connection(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class LakehouseResource(ConfigurableResource):
    endpoint: str
    region_name: str
    bucket_name: str
    access_key: str
    secret_key: str
    secure: Optional[bool] = False

    def get_client(self) -> Minio:
        client = Minio(
            endpoint=self.endpoint,
            region=self.region_name,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure,
        )

        if not client.bucket_exists(self.bucket_name):
            client.make_bucket(self.bucket_name)

        return client

    def get_storage_options(self) -> dict:
        options = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "aws_endpoint_url": "http://" + self.endpoint,
            "aws_region": self.region_name,
        }

        return options


class IcebergResource(ConfigurableResource):
    uri: str
    endpoint: str
    access_key: str
    secret_key: str
    secure: Optional[bool] = False
    impl: Optional[str] = "pyiceberg.io.pyarrow.PyArrowFileIO"

    def load_catalog(self, name: str) -> Catalog:
        def make_uri(uri: str):
            scheme = "https://" if self.secure else "http://"
            return scheme + uri.replace("https://", "").replace("http://", "")

        properties = {
            "uri": make_uri(self.uri),
            "s3.endpoint": make_uri(self.endpoint),
            "s3.secret-access-key": self.secret_key,
            "s3.access-key-id": self.access_key,
            "py-io-impl": self.impl
        }

        catalog = load_catalog(name, **properties)

        return catalog


class DbtResource(DbtCliResource):
    def __init__(self, project_dir=DBT_DIRECTORY, **kwargs):
        super().__init__(project_dir, **kwargs)
