from kafka import KafkaConsumer
import json
import os
from datetime import datetime

INVOICE_FILE = os.path.join(os.path.dirname(__file__), 'invoices/invoice_log.json')

def load_invoices():
    if os.path.exists(INVOICE_FILE):
        with open(INVOICE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_invoices(invoices):
    with open(INVOICE_FILE, 'w') as f:
        json.dump(invoices, f, indent=4)

def create_consumer():
    print("[Billing] Listening to 'order_created'...")
    return KafkaConsumer(
        'order_created',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='billing-group'
    )

def listen_to_events(consumer):
    invoices = load_invoices()

    for message in consumer:
        data = message.value
        invoice = {
            "product": data['product'],
            "quantity": data['quantity'],
            "total_cost": data.get('total_cost', 0),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        invoices.append(invoice)

        print(f"[✅ Billing] Invoice generated: {invoice['quantity']} x {invoice['product']} (₹{invoice['total_cost']})")
        save_invoices(invoices)

def main():
    consumer = create_consumer()
    listen_to_events(consumer)

if __name__ == "__main__":
    main()


