FROM bde2020/spark-python-template:3.3.0-hadoop3.3

COPY stock_transform.py /app/

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar \
    && wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar \
    && mv hadoop-aws-3.3.2.jar /spark/jars/ \
    && mv aws-java-sdk-bundle-1.11.1026.jar /spark/jars/

ENV MINIO_ROOT_USER=minio \
    MINIO_ROOT_PASSWORD=minio123 \
    SPARK_APPLICATION_PYTHON_LOCATION=/app/stock_transform.py \
    SPARK_APPLICATION_ARGS=stock-market/AAPL