FROM apache/spark:3.4.1

# ENV SPARK_APPLICATIONS_HOME=/opt/spark-apps
# ENV SPARK_MASTER_NAME=spark-hudi
# ENV SPARK_MASTER_PORT=7077
# ENV SPARK_MASTER_LOG=/spark/logs

ENV DERBY_HOME=/opt/db-derby-10.14.2.0-bin
ENV DERBY_VERSION=10.14.2.0
ENV SPARK_HOME=/opt/spark
ENV SPARK_VERSION=3.4

# Install basic utilities
USER root
RUN apt-get update && apt-get install -y wget

# Download Derby
RUN wget https://archive.apache.org/dist/db/derby/db-derby-${DERBY_VERSION}/db-derby-${DERBY_VERSION}-bin.tar.gz -P /opt/
RUN tar -xf /opt/db-derby-${DERBY_VERSION}-bin.tar.gz -C /opt/

# Download the appropriate hudi-spark bundle
RUN wget https://repository.apache.org/content/repositories/releases/org/apache/hudi/hudi-spark3.4-bundle_2.12/0.14.0/hudi-spark3.4-bundle_2.12-0.14.0.jar -P ${SPARK_HOME}/jars/

# Copy Derby jars to Spark jars so Thrift can use 'em
RUN cp $DERBY_HOME/lib/derby.jar       $SPARK_HOME/jars/
RUN cp $DERBY_HOME/lib/derbyclient.jar $SPARK_HOME/jars/

# Copy the entrypoint script which will spin up the Derby & Thrift servers
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
