#!/bin/bash

# Start Spark Master for pyspark to insert data through
$SPARK_HOME/bin/spark-class \
    org.apache.spark.deploy.master.Master \
    --ip $SPARK_MASTER_NAME \
    --port $SPARK_MASTER_PORT \
    --webui-port 8080 \
    &

# Start Derby server for the Hive metastore
$DERBY_HOME/bin/startNetworkServer &

# Start Thrift server pointing to Derby backend for the metastore
# and to hudi for the warehouse
$SPARK_HOME/sbin/start-thriftserver.sh \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog \
--conf spark.sql.warehouse.dir=/tmp/hudi/hive/warehouse \
--hiveconf hive.metastore.warehouse.dir=/tmp/hudi/hive/warehouse \
--hiveconf hive.metastore.schema.verification=false \
--hiveconf datanucleus.schema.autoCreateAll=true \
--hiveconf javax.jdo.option.ConnectionDriverName=org.apache.derby.jdbc.ClientDriver \
--hiveconf 'javax.jdo.option.ConnectionURL=jdbc:derby://localhost:1527/default;create=true' \
&

wait -n

python3 /usr/local/data/load.py || exit 1

echo "Waiting..."
sleep infinity
