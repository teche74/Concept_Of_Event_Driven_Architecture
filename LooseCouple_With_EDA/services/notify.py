from kafka import KafkaConsumer
import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs/notify_log.txt')

def log_notification(product, quantity):
    with open(LOG_FILE, 'a') as f:
        message = f"[{datetime.now()}] Notification: Order placed for {quantity} x {product}\n"
        f.write(message)
        print(message.strip())

def create_consumer():
    print("[Notify] Listening to 'order_created'...")
    return KafkaConsumer(
        'order_created',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='notify-group'
    )

def listen_to_events(consumer):
    for message in consumer:
        data = message.value
        log_notification(data['product'], data['quantity'])

def main():
    consumer = create_consumer()
    listen_to_events(consumer)

if __name__ == "__main__":
    main()
