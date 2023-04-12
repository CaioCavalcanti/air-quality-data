from platform import node, platform
from air_quality_orchestration.prefect import Spark
from prefect_gcp.cloud_storage import GcsBucket
from prefect import flow, task


@task(
    name="Check Data Lake",
    description="Checks the GCS Data Lake connection.",
    task_run_name="check-data-lake",
    tags=["task-type=health-check", "namespace=DataPlatform"],
    retries=3,
    retry_delay_seconds=5,
    log_prints=True,
)
def check_data_lake() -> GcsBucket:
    print("Checking GCS Bucket Data Lake...")

    data_lake_block = GcsBucket.load("data-lake")
    data_lake_block.get_bucket()

    print("GCS Bucket Data Lake: Healthy ✅")

    return data_lake_block


@task(
    name="Check Spark",
    description="Checks Spark connection and its connection to Data Lake.",
    task_run_name="check-spark",
    tags=["task-type=health-check", "namespace=DataPlatform"],
    retries=3,
    retry_delay_seconds=5,
    log_prints=True,
)
def check_spark(data_lake_bucket_name: str) -> None:
    print("Checking Spark...")

    spark_cluster_block = Spark.load("spark-cluster")
    spark_cluster_block.submit_job(
        job_path="health_check/health_check.py",
        args=[f"--data-lake-bucket-name={data_lake_bucket_name}"],
    )

    print("Spark: Healthy ✅")


@flow(
    name="Health Check",
    description="Check the health state of Prefect and installed blocks.",
    timeout_seconds=60,
    log_prints=True,
)
def check_health():
    print("Starting Health Check...")

    print(f"Network: {node()}")
    print(f"Instance: {platform()}")

    check_data_lake_task = check_data_lake.submit()
    check_spark(check_data_lake_task.result().bucket, wait_for=[check_data_lake_task])

    print("Health Check completed ✅")


if __name__ == "__main__":
    check_health()
