"""Provide utilities for orchestration via Prefect, such as custom blocks.
"""
from typing import List, MutableMapping, Optional
from google.api_core.operation import Operation
from google.api_core.client_options import ClientOptions
from google.cloud.dataproc import (
    JobControllerClient,
    SubmitJobRequest,
    Job,
    PySparkJob,
    JobPlacement,
)
from google.cloud.storage import Client, Bucket
from prefect.blocks.core import Block
from prefect import context


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

    def submit_job(self, job_path: str, args: Optional[List[str]] = None) -> Job:
        """Submits the Spark job on the given `job_path` to be executed in the Dataproc cluster.

        Args:
            job_path (str): the URL for the Spark job on the GCS bucket.
            args (List[str]): the arguments to pass when submitting the job.
        """
        submit_job_request = self._create_submit_job_request(job_path, args)
        operation = self._submit_job_as_operation(submit_job_request)

        return operation.result()

    def _get_spark_jobs_bucket(self) -> Bucket:
        gcs_client = Client()
        return gcs_client.get_bucket(self.gcp_gcs_spark_jobs_bucket_name)

    def _get_job_url(self, job_relative_path: str) -> str:
        return f"gs://{self.gcp_gcs_spark_jobs_bucket_name}/jobs/{job_relative_path}"

    def _get_full_label_key(self, key) -> str:
        return f"airquality-orchestration-prefect-{key}"

    def _get_job_labels(self) -> MutableMapping[str, str]:
        prefect_run_context = context.get_run_context()

        labels = {
            self._get_full_label_key("flow-run-id"): str(
                prefect_run_context.task_run.flow_run_id
            ),
            self._get_full_label_key("task-run-id"): str(
                prefect_run_context.task_run.id
            ),
        }

        return labels

    def _create_submit_job_request(
        self, job_path: str, args: Optional[List[str]] = None
    ) -> SubmitJobRequest:
        placement = JobPlacement(cluster_name=self.gcp_dataproc_cluster_name)
        labels = self._get_job_labels()
        pyspark_job = PySparkJob(
            main_python_file_uri=self._get_job_url(job_path), args=args
        )

        job = Job(placement=placement, pyspark_job=pyspark_job, labels=labels)

        submit_job_request = SubmitJobRequest(
            project_id=self.gcp_project_id, region=self.gcp_region, job=job
        )

        return submit_job_request

    def _submit_job_as_operation(self, request: SubmitJobRequest) -> Operation:
        client_options = ClientOptions(
            api_endpoint=f"{self.gcp_region}-dataproc.googleapis.com:443"
        )
        job_controller_client = JobControllerClient(client_options=client_options)

        return job_controller_client.submit_job_as_operation(request)
