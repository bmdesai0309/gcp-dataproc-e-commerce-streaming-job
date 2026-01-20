import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, expr
from pyspark.sql.types import *

CLICKSTREAM_SCHEMA = StructType([
        StructField("user_id", StructType(), True),
        StructField("session_id", StringType(), True),
        StructField("event_type", StringType(), True),  # 'view', 'add_to_cart', 'search'
        StructField("product_id", StringType(), True),
        StructField("page_url", StringType(), True),
        StructField("ip_address", StringType(), True),
        StructField("event_timestamp", TimestampType(), True)
    ])

def run_kafka_job():
    #Initialize Spark Session with kafka and BQ connectors
    spark = SparkSession.builder \
    .appName("Ecom-Clieckstream-Kafka-To-BQ") \
    .getOrCreate()

    #Register JAVA UDF
    spark.udf.registerJavaFunction("hash_udf", "com.ecommerce.spark.HashUDF")

    kafka_broker = "2.tcp.ngrok.io:14935"
    #Read from Kafka Topic
    kafka_options = {
        "kafka.bootstrap.servers": kafka_broker,
        "subscribe": "clickstream",
        "startingOffsets": "latest"
    }

    raw_stream = spark.readStream \
                    .format("kafka") \
                    .options(**kafka_options) \
                    .load()

    #Transform: JSON parsing & Anonymization (Logic)
    #Kafka stores value in binary; cast to string then parse JSON
    transformed_df = raw_stream.selectExpr("CAST(value as STRING)") \
                            .select(from_json(col("value"), CLICKSTREAM_SCHEMA).alias("data")) \
                            .select("data.*") \
                            .withColumn("user_id", expr("hash_udf(user_id)")) \
                            .withColumn("ip_address", expr("hash_udf(ip_address)"))

    query = transformed_df.writeStream \
        .format("bigquery") \
        .option("table", "ecommerce_analytics.fact_clickstream") \
        .option("checkpointLocation", "gs://gcp-dataproc-spark-code-bkd/checkpoints/kafka_job") \
        .option("temporaryGcsBucket", "gcp-dataproc-spark-code-bkd") \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    run_kafka_job()