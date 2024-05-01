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
    # table_path: str


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
        # table_path="/path/to/output/hudi/payment_table",
    ),
]

# This does not need to correspond to the `schema` from the DBT profile;
# it simply needs to correspond to the catalog that the external sources
# are configured under in the `sources.yaml` file.
HUDI_CATALOG = "hudi_sources"

HUDI_DEFAULTS = {
    "hoodie.datasource.write.operation": "insert",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
}

# I *believe* this needs to match the warehouse dir set in the run script
WAREHOUSE_DIR = "/tmp/hudi/hive/warehouse"


def main():
    spark = (
        SparkSession.builder
        .config("spark.jars.packages", "org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.hive.convertMetastoreParquet", "false")
        .config("conf spark.sql.warehouse.dir", WAREHOUSE_DIR)
        .getOrCreate()
    )

    spark.sql(f"create database if not exists {HUDI_CATALOG}")
    spark.sql(f"use {HUDI_CATALOG}")

    for source in SOURCES:
        filepath = str(Path(__file__).parent) + "/" + source.filename
        tablename = source.hudi_options["hoodie.table.name"]
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
            .save(f"{WAREHOUSE_DIR}/{tablename}")
        )

if __name__ == "__main__":
    main()
