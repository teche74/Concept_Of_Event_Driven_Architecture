from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    product = data.get('product')
    quantity = data.get('quantity')
    print(f"[NOTIFY] Sent order confirmation for {quantity} x {product}")
    return jsonify({"status": "success", "message": f"Notification sent for {product}"}), 200

if __name__ == "__main__":
    app.run(port=5002)
