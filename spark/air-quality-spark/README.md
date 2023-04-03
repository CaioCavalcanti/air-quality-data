# Air Quality Spark Python Package

This package provides an abstraction layer for Spark with the Lakehouse architecture using Delta Lake, making it easier to write Spark jobs in a standard way, including metadata columns to improve observability.

# Usage

## Loading from Raw to Base

```py
from air_quality_spark.spark_helper import LakehouseContext

context = LakehouseContext('data_lake_gcs_bucket_name')

# this will read parquet files from 'gs://data_lake_gcs_bucket_name/Raw/Events/'
raw_df = context.read_from_raw('Events/')

base_df = raw_df.select('date', 'type', 'value')

# this will write to 'gs://data_lake_gcs_bucket_name/Base/Events/'
context.write_to_base(base_df, 'Events/')
```

## Loading from Base to Transformed

```py
from air_quality_spark.spark_helper import LakehouseContext

context = LakehouseContext('data_lake_gcs_bucket_name')

# this will read a delta table from 'gs://data_lake_gcs_bucket_name/Base/Events/'
base_df = context.read_from_base('Events/')

transformed_df = raw_df.groupBy('date', 'type').sum('value')

# this will write to 'gs://data_lake_gcs_bucket_name/Transformed/DailyEvents/'
context.write_to_transformed(transformed_df, 'DailyEvents/')
```

# Publishing the package

```sh
export GCP_PROJECT_ID=<THE GCP PROJECT ID>
export REGION=<THE GCP REGION>
export REPOSITORY_NAME=python-${GCP_PROJECT_ID}
export REPOSITORY_URL=https://${REGION}-python.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY_NAME}/

# build the package
python ./setup.py bdist_wheel

# use the DevOps Service Account (the one used on the build agent) on GCP
gcloud auth activate-service-account --key-file=..\..\.gcp_keys\sa-devops-agent_gcp_key.json

# upload the package to the private repository
twine upload dist/* --repository-url ${REPOSITORY_URL}
```