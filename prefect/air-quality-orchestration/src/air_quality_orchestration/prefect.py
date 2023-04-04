"""Provide utilities for orchestration via Prefect, such as custom blocks.
"""
from google.cloud.storage import Client, Bucket
from prefect.blocks.core import Block


class Spark(Block):
    """A custom Prefect block used to handle Spark jobs on GCP Dataproc."""

    gcp_project_id: str
    gcp_region: str
    gcp_dataproc_cluster_name: str
    gcp_gcs_spark_jobs_bucket_name: str

    def upload_job(self, local_path: str, destination_path: str) -> str:
        """Upload a Spark job file to the GCS bucket used by the Dataproc cluster to submit jobs.

        Args:
            local_path (str): the file path for the Spark job.
            destination_path (str): the relative path for the job on the GCS bucket.

        Returns:
            str: a URL for the uploaded Spark job on the GCS bucket.
        """
        spark_jobs_bucket = self._get_spark_jobs_bucket()
        blob_path = f"jobs/{destination_path}"

        blob = spark_jobs_bucket.blob(blob_path)
        blob.upload_from_filename(local_path)

        blob_link = f"gs://{spark_jobs_bucket.name}/{blob_path}"

        return blob_link

    def submit_job(self, job_path, args):
        """Submits the Spark job on the given `job_path` to be executed in the Dataproc cluster.

        Args:
            job_path (_type_): the URL for the Spark job on the GCS bucket.
            args (_type_): the arguments to pass when submitting the job.
        """
        raise NotImplementedError

    def _get_spark_jobs_bucket(self) -> Bucket:
        client = Client()
        return client.get_bucket(self.gcp_gcs_spark_jobs_bucket_name)
