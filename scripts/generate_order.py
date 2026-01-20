import json
import time
import random
from google.cloud import pubsub_v1
from datetime import datetime

project_id = "learn-streaming"
topic_id = "ecommerce-orders"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def generate_order():
    return {
        "order_id": f"ORD_{random.randint(10000, 99999)}",
        "user_id": f"user_{random.randint(100, 999)}",
        "product_id": f"PROD_{random.randint(1, 50)}",
        "amount": round(random.uniform(20.0, 1000.0), 2),
        "currency": "USD",
        "status": "COMPLETED",
        "transaction_timestamp": datetime.now().isoformat()
    }

print("Publishing orders to GCP Pub/Sub...")
while True:
    order = generate_order()
    data = json.dumps(order).encode("utf-8")
    publisher.publish(topic_path, data)
    print(f"Sent: {order['order_id']}")
    time.sleep(3) # Send an order every 3 seconds