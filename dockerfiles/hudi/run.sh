#!/bin/bash

# Start Spark master and worker
/${SPARK_HOME}/bin/spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_NAME --port $SPARK_MASTER_PORT --webui-port 8080 &
/${SPARK_HOME}/bin/spark-class org.apache.spark.deploy.worker.Worker spark://$SPARK_MASTER_NAME:$SPARK_MASTER_PORT --webui-port 8081 &
/${SPARK_HOME}/sbin/start-thriftserver.sh &
wait
