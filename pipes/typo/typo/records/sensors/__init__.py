from datetime import datetime
from dagster import sensor
from dagster import (
    SkipReason,
    RunRequest,
    SensorEvaluationContext,
    DefaultSensorStatus,
)

from dagster_aws.s3.sensor import get_s3_keys
from typo.shared.resources import StorageResource
from typo.records.jobs import lakehouse_records_job, warehouse_records_job


@sensor(
    jobs=[lakehouse_records_job, warehouse_records_job],
    default_status=DefaultSensorStatus.STOPPED,
    minimum_interval_seconds=60 * 5,
)
def storage_records_sensor(context: SensorEvaluationContext, storage: StorageResource):
    since_key = context.cursor or None
    partition = datetime.utcnow().strftime("%Y-%m")  # TODO : queue
    new_s3_keys = get_s3_keys(
        storage.bucket_name,
        prefix=f"records/{partition}",
        since_key=since_key,
    )

    if not new_s3_keys:
        return SkipReason(f"No new objects found for bucket {storage.bucket_name}")

    def create_config(s3_key: str):
        records, partition, user_id, filename, *_ = s3_key.split("/")
        records, timestamp, *_, extension = filename.split(".")
        date = datetime.fromisoformat(timestamp).date()

        return {
            "key": s3_key,
            "user_id": user_id,
            "partition": partition,
            "timestamp": timestamp,
            "date": str(date),
        }

    lakehouse_requests = [
        RunRequest(
            run_key=f"lakehouse_{s3_key}",
            job_name="lakehouse_records_job",
            run_config={"ops": {"lakehouse_records": {"config": create_config(s3_key)}}}
        )
        for s3_key in new_s3_keys
    ]

    warehouse_requests = [
        RunRequest(
            run_key=f"warehouse_{s3_key}",
            job_name="warehouse_records_job",
            run_config={"ops": {"warehouse_records": {"config": create_config(s3_key)}}}
        )
        for s3_key in new_s3_keys
    ]

    context.update_cursor(new_s3_keys.pop())
    return lakehouse_requests + warehouse_requests
