"""
Provide helper classes to work with the Lakehouse on Spark jobs without the heavy lifting.
"""

from datetime import datetime
from enum import Enum
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F


class DataLakeLayer(Enum):
    """The data layers available on the Data Laker, following the medallion architecture."""

    RAW = "Raw"
    BASE = "Base"
    TRANSFORMED = "Transformed"


class LakehouseContext:
    """Wraps a SparkSession and provide the abstractions required to work
    on the lakehouse, enabling read/write from/to Raw, Base and Transformed
    layers, while hiding the implementation details.
    """

    def __init__(self, data_lake_bucket_name: str) -> None:
        self._data_lake_bucket_name = data_lake_bucket_name
        self._spark = self._get_or_create_spark_session()

    @property
    def spark(self) -> SparkSession:
        """The current :class:`pyspark.sql.SparkSession` running on the context."""
        return self._spark

    def read_from_raw(self, relative_path: str) -> DataFrame:
        """Reads a dataset in parquet format from the Raw layer of the Lakehouse.

        Args:
            relative_path (str): the relative path of the dataset.
            For example `AirQuality/Dimensions/Uur/*`.

        Returns:
            DataFrame: the dataset loaded on a :class:`pyspark.sql.DataFrame`.
        """
        full_raw_path = self._get_data_lake_url(DataLakeLayer.RAW, relative_path)

        return self.spark.read.parquet(full_raw_path)

    def read_from_base(self, relative_path: str) -> DataFrame:
        """Reads a dataset in Delta format from the Base layer of the Lakehouse.

        Args:
            relative_path (str): the relative path of the dataset.
            For example `AirQuality/Dimensions/Hour/`.

        Returns:
            DataFrame: the dataset loaded on a :class:`pyspark.sql.DataFrame`.
        """
        return self._read_delta_table(DataLakeLayer.BASE, relative_path)

    def read_from_transformed(self, relative_path: str) -> DataFrame:
        """Reads a dataset in Delta format from the Transformed layer of the Lakehouse.

        Args:
            relative_path (str): the relative path of the dataset.
            For example `AirQuality/DailyAirQuality/`.

        Returns:
            DataFrame: the dataset loaded on a :class:`pyspark.sql.DataFrame`.
        """
        return self._read_delta_table(DataLakeLayer.TRANSFORMED, relative_path)

    def write_to_base(self, base_df: DataFrame, relative_path: str) -> None:
        """Writes the given :class:`pyspark.sql.DataFrame` as a Delta table into the
        Base layer of the Lakehouse.

        Args:
            base_df (DataFrame): the dataset to write into the Base layer.
            path (relative_path): the relative path of the dataset on the Base layer.
        """
        full_path = self._get_data_lake_url(DataLakeLayer.BASE, relative_path)
        self._write_delta_table(base_df, full_path)

    def write_to_transformed(
        self, transformed_df: DataFrame, relative_path: str
    ) -> None:
        """Writes the given :class:`pyspark.sql.DataFrame` as a Delta table into the
        Transformed layer of the Lakehouse.

        Args:
            transformed_df (DataFrame): the dataset to write into the Transformed layer.
            relative_path (str): the relative path of the dataset on the Transformed layer.
        """
        full_path = self._get_data_lake_url(DataLakeLayer.TRANSFORMED, relative_path)
        self._write_delta_table(transformed_df, full_path)

    def _write_delta_table(self, df_to_write: DataFrame, full_table_path: str) -> None:
        annotated_df = self._annotate_df(df_to_write)

        # for testing purpose and keep it simple we will overwrite, but on
        # a production scenario we also need to handle schema changes and
        # most likely use merge/append mode instead.
        annotated_df.write.format("delta").mode("overwrite").save(full_table_path)

    def _annotate_df(self, df_to_annotate: DataFrame) -> DataFrame:
        """Include metadata columns to improve observability:

        `__effective_timestamp`: the datetime (UTC) in which the dataset was processed.
        `__effective_origin`: the Spark Application ID that processed the dataset.

        Args:
            df_to_annotate (:class:`pyspark.sql.DataFrame`): the DataFrame to annotate.

        Returns:
            DataFrame: the given :class:`pyspark.sql.DataFrame` with the additional
            metadata columns.
        """

        effective_timestamp = datetime.utcnow()
        effective_origin = f"spark:{self.spark.sparkContext.applicationId}"

        return df_to_annotate.withColumn(
            "__effective_timestamp", F.lit(effective_timestamp)
        ).withColumn("__effective_origin", F.lit(effective_origin))

    def _get_or_create_spark_session(self) -> SparkSession:
        return SparkSession.builder.appName("AirQuality").getOrCreate()

    def _get_data_lake_url(self, layer: DataLakeLayer, path: str) -> str:
        return f"gs://{self._data_lake_bucket_name}/{layer.value}/{path}"

    def _read_delta_table(self, layer: DataLakeLayer, table_path: str) -> DataFrame:
        full_table_path = self._get_data_lake_url(layer, table_path)

        return self.spark.read.format("delta").load(full_table_path)
