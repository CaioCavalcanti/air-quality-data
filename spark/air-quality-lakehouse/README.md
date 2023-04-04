# Air Quality Lakehouse Python Package

This package provides an abstraction layer for Spark with the Lakehouse architecture using Delta Lake, making it easier to write Spark jobs in a standard way, including metadata columns to improve observability.

# Usage

## Loading from Raw to Base

```py
from air_quality_lakehouse.context import LakehouseContext

context = LakehouseContext('data_lake_gcs_bucket_name')

# this will read parquet files from 'gs://data_lake_gcs_bucket_name/Raw/Events/'
raw_df = context.read_from_raw('Events/')

base_df = raw_df.select('date', 'type', 'value')

# this will write to 'gs://data_lake_gcs_bucket_name/Base/Events/'
context.write_to_base(base_df, 'Events/')
```

## Loading from Base to Transformed

```py
from air_quality_lakehouse.context import LakehouseContext

context = LakehouseContext('data_lake_gcs_bucket_name')

# this will read a delta table from 'gs://data_lake_gcs_bucket_name/Base/Events/'
base_df = context.read_from_base('Events/')

transformed_df = raw_df.groupBy('date', 'type').sum('value')

# this will write to 'gs://data_lake_gcs_bucket_name/Transformed/DailyEvents/'
context.write_to_transformed(transformed_df, 'DailyEvents/')
```

## Accessing SparkSession

```py
from air_quality_lakehouse.context import LakehouseContext

context = LakehouseContext('data_lake_gcs_bucket_name')

spark = context.spark
```
