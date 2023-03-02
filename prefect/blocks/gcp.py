from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GCS
import os


def create_data_lake_block() -> GcsBucket:
    block_name = "data-lake"
    data_lake_bucket_name = os.getenv('GCP_GCS_DATA_LAKE_BUCKET_NAME')

    print(f"\tCreating GcsBucket block '{block_name}'...")

    if not data_lake_bucket_name:
        raise ValueError(
            "Missing required environment variable 'GCP_GCS_DATA_LAKE_BUCKET_NAME'.")

    block = GcsBucket(bucket=data_lake_bucket_name)
    block.save(block_name, overwrite=True)

    print(f"\tGcsBucket block '{block_name}' created!")


def create_flows_storage_block() -> GCS:
    block_name = "flows-storage"
    flows_storage_bucket_name = os.getenv('GCP_GCS_FLOWS_STORAGE_BUCKET_NAME')

    print(f"\tCreating GCS block '{block_name}'...")

    if not flows_storage_bucket_name:
        raise ValueError(
            "Missing required environment variable 'GCP_GCS_FLOWS_STORAGE_BUCKET_NAME'.")

    block = GCS(bucket_path=f"{flows_storage_bucket_name}/flows/")
    block.save(block_name, overwrite=True)

    print(f"\tGCS block '{block_name}' created!")


def create_gcp_blocks():
    print("Creating GCP blocks...")

    create_data_lake_block()
    create_flows_storage_block()

    print("GCP blocks created!")


if __name__ == '__main__':
    create_gcp_blocks()
