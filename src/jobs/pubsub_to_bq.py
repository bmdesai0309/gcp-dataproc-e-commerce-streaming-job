import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *


ORDER_SCHEMA = StructType([
    StructField("order_id", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("product_id", StringType(), False),
    StructField("amount", DoubleType(), False),
    StructField("currency", StringType(), True),
    StructField("status", StringType(), False),
    StructField("transaction_timestamp", TimestampType(), False)
])


def run_pubsub_job():
    spark = SparkSession.builder \
        .appName("Ecom-Orders-PubSub-Streaming") \
        .getOrCreate()

    # Configuration from Environment Variables
    project_id = os.environ.get('PROJECT_ID', 'learn-streaming')
    bucket_name = "gcp-dataproc-spark-code-bkd"
    subscription_path = f"projects/{project_id}/subscriptions/ecommerce-orders-sub"

    # 1. Read from Pub/Sub
    # The 'pubsub' format is natively supported in Dataproc
    df = spark.readStream \
        .format("pubsub") \
        .option("subscription", subscription_path) \
        .load()

    # 2. Transform: Convert binary data to String and Parse JSON
    orders_df = df.selectExpr("CAST(data AS STRING)") \
        .select(from_json(col("data"), ORDER_SCHEMA).alias("order_data")) \
        .select("order_data.*")

    # 3. Write to BigQuery with Production Options
    query = orders_df.writeStream \
        .format("bigquery") \
        .option("table", "ecommerce_analytics.fact_orders") \
        .option("checkpointLocation", f"gs://{bucket_name}/checkpoints/pubsub_orders") \
        .option("temporaryGcsBucket", bucket_name) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    run_pubsub_job()