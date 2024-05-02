from dataclasses import dataclass
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DecimalType,
    TimestampType,
)


@dataclass
class DataSource:
    filename: str
    hudi_options: dict
    schema: StructType


SOURCES = [
    DataSource(
        filename="payments.csv",
        hudi_options = {
            "hoodie.table.name": "payment",
            "hoodie.datasource.write.recordkey.field": "payment_id",
        },
        schema=StructType([
            StructField("payment_id", IntegerType(), nullable=False),
            StructField("customer_id", IntegerType(), nullable=False),
            StructField("staff_id", IntegerType(), nullable=False),
            StructField("rental_id", IntegerType(), nullable=False),
            StructField("amount", DecimalType(), nullable=False),
            StructField("payment_date", TimestampType(), nullable=False),
        ]),
    ),
]

# This does not need to correspond to the `schema` from the DBT profile;
# it simply needs to correspond to the catalog that the external sources
# are configured under in the `sources.yaml` file.
HUDI_CATALOG = "hudi_sources"

HUDI_DEFAULTS = {
    # Use "insert" rather than "upsert" since the table write modes are
    # set to "overwrite" rather than "append". There did not seem to be
    # value in having slightly more complicated upsert logic (requiring
    # partition key, etc. configuration) for what is static fixture data.
    "hoodie.datasource.write.operation": "insert",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
}

# This needs to match the warehouse dir set in the run script
WAREHOUSE_DIR = "/tmp/hudi/hive/warehouse"


def main():
    spark = (
        SparkSession.builder
        .enableHiveSupport()
        .config("spark.jars.packages", "org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.warehouse.dir", WAREHOUSE_DIR)
        # These need to match the configuration for Derby/Thrift in the `run.sh` script
        .config("javax.jdo.option.ConnectionDriverName", "org.apache.derby.jdbc.ClientDriver")
        .config("javax.jdo.option.ConnectionURL", "jdbc:derby://localhost:1527/default;create=true")
        .getOrCreate()
    )

    spark.sql(f"create database if not exists {HUDI_CATALOG}")
    spark.sql(f"use {HUDI_CATALOG}")

    print("Found the following databases in the metastore:")
    spark.sql("show databases").show()

    for source in SOURCES:
        filepath = str(Path(__file__).parent) + "/" + source.filename
        (
            spark
            .read
            .format("csv")
            .option("header", "true")
            .schema(source.schema)
            .load(filepath)
            .write
            .format("org.apache.hudi")
            .options(**{**HUDI_DEFAULTS, **source.hudi_options})
            .mode("overwrite")
            .saveAsTable(
                f"{HUDI_CATALOG}.payment",
                format="parquet",
                mode="overwrite",
            )
        )

if __name__ == "__main__":
    main()
