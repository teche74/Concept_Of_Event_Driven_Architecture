from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json()
    product = data.get('product')
    quantity = data.get('quantity')
    print(f"[INVENTORY] Reduce stock: {quantity} x {product}")
    return jsonify({"status": "success", "message": f"Inventory updated for {product}"}), 200

if __name__ == "__main__":
    app.run(port=5001)
