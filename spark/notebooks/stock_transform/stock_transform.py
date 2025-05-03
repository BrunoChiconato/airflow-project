from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import explode, arrays_zip, from_unixtime
from pyspark.sql.types import DateType

import os
import sys


if __name__ == '__main__':

    def app():
        spark = (
            SparkSession.builder.appName("FormatStock")
            .config("fs.s3a.access.key", os.getenv("MINIO_ROOT_USER", "minio"))
            .config("fs.s3a.secret.key", os.getenv("MINIO_ROOT_PASSWORD", "minio123"))
            .config("fs.s3a.endpoint", "http://minio:9000")
            .config("fs.s3a.path.style.access", "true")
            .config("fs.s3a.connection.ssl.enabled", "false")
            .getOrCreate()
        )

        df = spark.read.option("header", "false") \
            .json(f"s3a://{os.getenv('SPARK_APPLICATION_ARGS')}/prices.json")

        df_exploded = df.select("timestamp", explode("indicators.quote").alias("quote")) \
            .select("timestamp", "quote.*")

        df_zipped = df_exploded.select(arrays_zip("timestamp", "close", "high", "low", "open", "volume").alias("zipped"))
        df_zipped = df_zipped.select(explode("zipped")).select("col.timestamp", "col.close", "col.high", "col.low", "col.open", "col.volume")
        df_zipped = df_zipped.withColumn('date', from_unixtime('timestamp').cast(DateType()))

        df_zipped.write \
            .mode("overwrite") \
            .option("header", "true") \
            .option("delimiter", ",") \
            .csv(f"s3a://{os.getenv('SPARK_APPLICATION_ARGS')}/formatted_prices")

    app()

    os.system('kill %d' % os.getpid())