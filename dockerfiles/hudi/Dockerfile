FROM apache/spark:3.4.1

# ENV SPARK_HOME=/opt/spark
# ENV SPARK_APPLICATIONS_HOME=/opt/spark-apps
# ENV SPARK_MASTER_NAME=spark-hudi
# ENV SPARK_MASTER_PORT=7077
# ENV SPARK_MASTER_LOG=/spark/logs

# Install basic utilities
USER root
RUN apt-get update && apt-get install -y wget

# Download and install Apache Hudi - 0.14.x is built against Spark 3.4.x
#
# See:
#   https://mvnrepository.com/artifact/org.apache.hudi/hudi-spark3.4-bundle_2.12/0.14.1
#   https://hudi.apache.org/docs/quick-start-guide/#spark-3-support-matrix
RUN wget https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3.4-bundle_2.12/0.14.1/hudi-spark3.4-bundle_2.12-0.14.1.jar -P ${SPARK_HOME}/jars/

# Copy the entrypoint script
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Expose ports (4040- Spark UI, 7077- Spark master, 8020- HDFS, 50070- HDFS UI)
EXPOSE 4040 7077 8020 50070

# Entry point
CMD ["/run.sh"]
