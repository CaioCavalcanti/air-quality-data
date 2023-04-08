"""Provide utilities for orchestration via Prefect, such as custom blocks.
"""
from google.cloud.dataproc_v1 import JobControllerClient
from google.cloud.dataproc_v1.types import Job
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

        blob_link = self._get_job_url(destination_path)

        return blob_link

    def submit_job(self, job_path, args) -> Job:
        """Submits the Spark job on the given `job_path` to be executed in the Dataproc cluster.

        Args:
            job_path (_type_): the URL for the Spark job on the GCS bucket.
            args (_type_): the arguments to pass when submitting the job.
        """
        job_client = JobControllerClient(
            client_options={
                "api_endpoint": f"{self.gcp_region}-dataproc.googleapis.com:443"
            }
        )

        job_uri = self._get_job_url(job_path)

        job = {
            "placement": {"cluster_name": self.gcp_dataproc_cluster_name},
            "pyspark_job": {"main_python_file_uri": job_uri, "args": args},
        }

        operation = job_client.submit_job_as_operation(
            request={
                "project_id": self.gcp_project_id,
                "region": self.gcp_region,
                "job": job,
            }
        )

        return operation.result()

    def _get_spark_jobs_bucket(self) -> Bucket:
        client = Client()
        return client.get_bucket(self.gcp_gcs_spark_jobs_bucket_name)

    def _get_job_url(self, job_relative_path: str) -> str:
        return f"gs://{self.gcp_gcs_spark_jobs_bucket_name}/jobs/{job_relative_path}"
