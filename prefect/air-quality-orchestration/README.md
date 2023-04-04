# Air Quality Orchestration Python Package

This package provides

# Usage

## Adding the Spark block to Prefect

```py
from air_quality_orchestration.prefect import Spark

spark_block = Spark(
    gcp_project_id="<THE GCP PROJECT ID WHERE THE SPARK CLUSTER IS HOSTED>",
    gcp_project_region="<THE GCP REGION WHERE THE SPARK CLUSTER IS HOSTED>",
    gcp_dataproc_cluster_name="<THE NAME OF THE GCP DATAPROC CLUSTER>",
    gcp_gcs_spark_jobs_bucket_name="<THE NAME OF THE GCS BUCKET TO UPLOAD SPARK JOBS>")

spark_block.save("MySparkBlock")
```

## Uploading Spark Job file

```py
from air_quality_orchestration.prefect import Spark

spark_block = Spark.load("MySparkBlock")
spark_block.upload_job("/spark_jobs/my_spark_job.py", "MyPackage/my_spark_job.py")
```

## Submiting Spark Jobs

```py
from air_quality_orchestration.prefect import Spark

job_path = "MyPackage/my_spark_job.py"
args = [
    "--my-job-arg=42"
]

spark_block = Spark.load("MySparkBlock")
spark_block.submit_job(job_path, args)
```
