from pyspark.sql.types import *

#Kafka clickstream schema
CLICKSTREAM_SCHEMA = StructType([
    StructField("user_id", StructType(), True),
    StructField("session_id", StringType(), True),
    StructField("event_type", StringType(), True),  # 'view', 'add_to_cart', 'search'
    StructField("product_id", StringType(), True),
    StructField("page_url", StringType(), True),
    StructField("ip_address", StringType(), True),
    StructField("event_timestamp", TimestampType(), True)
])

#pub/sub order schema
ORDER_SCHEMA = StructType([
    StructField("order_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("status", StringType(), True),      # 'completed', 'cancelled'
    StructField("transaction_timestamp", TimestampType(), True)
])