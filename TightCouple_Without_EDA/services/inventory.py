from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
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

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    items = load_items()
    if not items:
        print("[Inventory] No items found in the database. Exiting...")
        return jsonify({"status": "error", "message": "No items found"}), 404

    data = request.get_json()
    product = data.get('product')
    quantity = data.get('quantity')

    if product not in items:
        print(f"Product '{product}' not found in inventory.")
        return jsonify({"status": "error", "message": f"Product '{product}' not found"}), 404

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"status": "error", "message": "Invalid quantity"}), 400

    stock = items[product]['stock']
    if stock < quantity:
        print(f"[Inventory] Insufficient stock for {product}. Current stock: {stock}, Requested: {quantity}")
        return jsonify({"status": "error", "message": "Insufficient stock"}), 400

    items[product]['stock'] -= quantity
    save_items(items)

    print(f"[INVENTORY] {product} stock reduced by {quantity}. Remaining: {items[product]['stock']}")
    return jsonify({"status": "success", "message": f"Inventory updated for {product}"}), 200

if __name__ == "__main__":
    app.run(port=5001)
