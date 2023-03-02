from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(
    name="Check Data Lake",
    description="Checks the GCS Data Lake connection.",
    task_run_name="check-gcs-data-lake",
    tags=["health-check"],
    retries=3,
    retry_delay_seconds=5,
    log_prints=True
)
def check_gcs_data_lake():
    data_lake_block = GcsBucket.load("data-lake")
    bucket = data_lake_block.get_bucket()

    print(f"GCS Bucket Data Lake: Healthy")


@flow(
    name="Health Check",
    description="Check the health state of Prefect and installed blocks.",
    timeout_seconds=60,
    log_prints=True
)
def check_health():
    check_gcs_data_lake()


if __name__ == '__main__':
    check_health()
