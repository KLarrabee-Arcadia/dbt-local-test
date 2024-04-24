FROM apache/spark:3.4.1

# Copy the entrypoint script
COPY run.sh /run.sh

USER root
RUN chmod +x /run.sh

# Expose ports (4040- Spark UI, 7077- Spark master, 8020- HDFS, 50070- HDFS UI)
EXPOSE 4040 7077 8020 50070

# Entry point
CMD ["/run.sh"]
