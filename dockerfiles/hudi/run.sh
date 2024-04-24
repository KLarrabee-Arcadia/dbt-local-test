#!/bin/bash

# Start Derby server
#
# `startNetworkServer` doesn't appear to be able to be sent to the background with `&`
# so using `nohup` appears to be necessary. The main downside is that this redirects
# output so docker logs will not show it.
$DERBY_HOME/bin/startNetworkServer -h 0.0.0.0 &

# Start Thrift server pointing to Derby backend
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

sleep infinity
