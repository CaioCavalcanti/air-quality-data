from datetime import datetime
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(
    name="Check Data Lake",
    description="Checks the GCS Data Lake connection.",
    task_run_name="check-gcs-data-lake",
    tags=["health-check"],
    retries=3,
    retry_delay_seconds=5,
)
def check_gcs_data_lake():
    data_lake_block = GcsBucket.load("data-lake")
    assert data_lake_block.get_bucket().exists()


@flow(
    name="Health Check",
    description="Check the health state of Prefect and installed blocks.",
    flow_run_name="health-check-on-{date:%Y-%m-%dT%H:%M:%S}",
    timeout_seconds=60
)
def check_health(date: datetime):
    print('all good!')
    check_gcs_data_lake()


if __name__ == '__main__':
    check_health(datetime.utcnow())
