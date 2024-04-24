#!/bin/bash

export SPARK_VERSION=3.4

# This will download the hudi-spark3.4 bundle
${SPARK_HOME}/bin/spark-shell \
    --packages org.apache.hudi:hudi-spark${SPARK_VERSION}-bundle_2.12:0.14.1                 \
    --conf 'spark.serializer=org.apache.spark.serializer.KryoSerializer'                     \
    --conf 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog' \
    --conf 'spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension'      \
    --conf 'spark.kryo.registrator=org.apache.spark.HoodieSparkKryoRegistrar'                \
    || exit 1

# Start Spark master and worker
${SPARK_HOME}/bin/spark-class \
    org.apache.spark.deploy.master.Master \
    --ip $SPARK_MASTER_NAME               \
    --port $SPARK_MASTER_PORT             \
    --webui-port 8080                     \
    &

${SPARK_HOME}/bin/spark-class \
    org.apache.spark.deploy.worker.Worker         \
    spark://$SPARK_MASTER_NAME:$SPARK_MASTER_PORT \
    --webui-port 8081                             \
    &

# Start Thrift server for connecting to Spark cluster with DBT
${SPARK_HOME}/sbin/start-thriftserver.sh

wait
