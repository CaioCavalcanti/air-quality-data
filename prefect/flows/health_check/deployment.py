from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.filesystems import GCS
from main_flow import check_health
from devtools import debug
import os


def upload_flow_directory(flows_storage_block: GCS) -> str:
    if not flows_storage_block:
        raise ValueError("Missing required flows_storage_block")

    source_path = os.path.dirname(os.path.abspath(__file__))
    destination_relative_path = "/health_check/"

    print(
        f"Uploading flow code from '{source_path}' to '{flows_storage_block}/{destination_relative_path}'...")

    flows_storage_block.put_directory(
        local_path=source_path,
        to_path=destination_relative_path,
        ignore_file=f"{source_path}/.prefectignore")

    print(
        f"Flow code uploaded to '{flows_storage_block}/{destination_relative_path}'!")

    return destination_relative_path


def create_deployment(flows_storage_block: GCS, destination: str) -> None:
    if not flows_storage_block:
        raise ValueError("Missing required flows_storage_block")

    deployment_name = "Hourly Health Check"
    
    print(f"Creating deployment '{deployment_name}' for flow '{check_health.name}'...")
    
    every_hour_cron = CronSchedule(
        cron="0 */1 * * *", timezone="Europe/Amsterdam")

    deployment = Deployment.build_from_flow(
        flow=check_health,
        name=deployment_name,
        schedule=every_hour_cron,
        storage=flows_storage_block,
        path=destination,
        tags=['health-check'],
        skip_upload=True
    )

    deployment_id = deployment.apply()
    
    debug(deployment)
    print(f"Deployment created: {deployment_id}")


def deploy(upload_flow: bool) -> None:
    storage_block = GCS.load("flows-storage")

    if upload_flow:
        destination = upload_flow_directory(storage_block)

    create_deployment(storage_block, destination)


if __name__ == '__main__':
    deploy(upload_flow=True)
