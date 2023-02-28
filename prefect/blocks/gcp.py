from prefect_gcp.cloud_storage import GcsBucket
import os

def create_data_lake_block() -> GcsBucket:
    data_lake_bucket_name = os.getenv('DATA_LAKE_GCS_BUCKET_NAME')
    
    if not data_lake_bucket_name:
        raise ValueError("Missing required environment variable 'DATA_LAKE_GCS_BUCKET_NAME'.")
    
    return GcsBucket(bucket=data_lake_bucket_name)

def create_gcp_blocks():
    create_data_lake_block().save("data-lake", overwrite=True)

if __name__ == '__main__':
    create_gcp_blocks()