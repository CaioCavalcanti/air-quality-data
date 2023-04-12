import argparse
from air_quality_lakehouse.context import LakehouseContext


def main(data_lake_bucket_name: str) -> None:
    context = LakehouseContext(data_lake_bucket_name)

    context.spark.sql("CREATE TEMPORARY VIEW temp_health_check AS SELECT 1")
    context.spark.catalog.tableExists("temp_health_check")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-lake-bucket-name", required=True)

    args = parser.parse_args()

    main(args.data_lake_bucket_name)
