from kafka import KafkaConsumer
import json
import os

ITEM_FILE = os.path.join(os.path.dirname(__file__), '../../items_db/items.json')


def load_items():
    try:
        with open(ITEM_FILE, 'r') as file:
            items = json.load(file)
            return items
    except FileNotFoundError:
        print(f"Error: The file {ITEM_FILE} does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {ITEM_FILE} is not a valid JSON.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
    
def save_items(items):
    try:
        with open(ITEM_FILE, 'w') as file:
            json.dump(items, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving items: {e}")

def CreateConsumer():
    print("[Inventory] Listening to 'order_created' events...")
    return KafkaConsumer(
        'order_created',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='inventory-group'
    )


def listen_to_events(consumer):
    items = load_items()
    if not items:
        print("[Inventory] No items found in the database. Exiting...")
        return
    
    for message in consumer:
        data = message.value
        product = data['product']
        quantity = int(data['quantity'])
        stock = items[product]['stock']
        if product not in items:
            print(f"Product '{product}' not found in inventory.")
            continue
        if stock < quantity:
            print(f"[Inventory] Insufficient stock for {data['product']}. Current stock: {items[data['product']]['stock']}, Requested: {data['quantity']}")
            continue
        
        items[product]['stock'] -= quantity
        print(f"Stock updated: {product} → {items[product]['stock']} left")
        save_items(items)

def main():
    inventory_consumer = CreateConsumer()
    listen_to_events(inventory_consumer)

if __name__ == "__main__":
    main()