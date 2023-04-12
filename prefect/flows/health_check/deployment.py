import os
from air_quality_orchestration.prefect import Spark
from main_flow import check_health
from prefect.deployments import Deployment
from prefect.infrastructure import KubernetesJob
from prefect.server.schemas.schedules import CronSchedule
from prefect.filesystems import GCS


def upload_flow_code(flows_storage_block: GCS) -> str:
    if not flows_storage_block:
        raise ValueError("Missing required flows_storage_block")

    source_path = os.path.dirname(os.path.abspath(__file__))
    destination_relative_path = "health_check/"
    full_path = "{flows_storage_block.bucket_path}{destination_relative_path}"

    print(f"Uploading flow code from '{source_path}' to '{full_path}'...")

    flows_storage_block.put_directory(
        local_path=source_path,
        to_path=destination_relative_path,
        ignore_file=f"{source_path}/.prefectignore",
    )

    print(
        f"Flow code uploaded to '{flows_storage_block.bucket_path}{destination_relative_path}'!"
    )

    return destination_relative_path


def upload_spark_jobs() -> None:
    spark_block = Spark.load("spark-cluster")

    spark_block.upload_job(
        local_path="./spark_jobs/health_check.py",
        destination_path="health_check/health_check.py",
    )


def create_deployment(flows_storage_block: GCS, destination: str) -> None:
    if not flows_storage_block:
        raise ValueError("Missing required flows_storage_block")

    deployment_name = "Hourly Health Check"

    print(f"Creating deployment '{deployment_name}' for flow '{check_health.name}'...")

    every_hour_cron = CronSchedule(cron="0 */1 * * *", timezone="Europe/Amsterdam")

    k8s_job = KubernetesJob.load("k8s-job")

    deployment = Deployment.build_from_flow(
        flow=check_health,
        name=deployment_name,
        schedule=every_hour_cron,
        infrastructure=k8s_job,
        storage=flows_storage_block,
        path=destination,
        entrypoint=f"main_flow.py:{check_health.__name__}",
        tags=["health-check"],
        skip_upload=True,
    )

    deployment_id = deployment.apply()

    print(f"Deployment created: {deployment_id}")


def deploy(upload_flow: bool) -> None:
    storage_block = GCS.load("flows-storage")

    if upload_flow:
        upload_spark_jobs()
        destination = upload_flow_code(storage_block)

    create_deployment(storage_block, destination)


if __name__ == "__main__":
    deploy(upload_flow=True)
