import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9091'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event_types = ['view', 'add_to_cart', 'search', 'click']
product_ids = [f'PROD_{i}' for i in range(1, 20)]

def generate_click():
    return {
        "user_id": f"USER_{random.randint(100, 999)}",
        "session_id": f"sess_{random.getrandbits(32)}",
        "event_type": random.choice(event_types),
        "product_id": random.choice(product_ids),
        "page_url": "https://mystore.com/shop",
        "ip_address": f"192.168.1.{random.randint(1, 255)}",
        "event_timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("Starting local kafka producer (Clickstream) .....")
    try:
        while True:
            event = generate_click()
            producer.send('clickstream', value=event)
            print(f"Sent: {event['event_type']} for {event['product_id']}")
            time.sleep(0.5)  # Simulate real-time flow
    except KeyboardInterrupt:
        print("Stopping producer.")
