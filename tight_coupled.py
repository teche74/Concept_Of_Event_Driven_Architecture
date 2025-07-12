from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)


# --- SERVICE CALLS ---
def update_inventory(product, quantity):
    try:
        print("makeing request :")
        res = requests.post("http://localhost:5001/update_inventory", json={
            "product": product,
            "quantity": quantity
        })
        return res.ok
    except Exception as e:
        print(f"Inventory Error: {e}")
        return False

def send_notification(product, quantity):
    try:
        res = requests.post("http://localhost:5002/send_notification", json={
            "product": product,
            "quantity": quantity
        })
        return res.ok
    except Exception as e:
        print(f"Notification Error: {e}")
        return False

def create_invoice(product, total_cost):
    try:
        res = requests.post("http://localhost:5003/create_invoice", json={
            "product": product,
            "total_cost": total_cost
        })
        return res.ok
    except Exception as e:
        print(f"Billing Error: {e}")
        return False


def retry_request(url, payload, retries=3, delay=1):
    for _ in range(retries):
        try:
            res = requests.post(url, json=payload, timeout=3)
            if res.ok:
                return True
        except Exception as e:
            print(f"Retry failed: {e}")
        time.sleep(delay)
    return False

# --- MAIN ORDER ENDPOINT ---
@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    product = data.get("product")
    quantity = data.get("item_count")
    total_cost = data.get("total_cost")
    
    
    inv_status = update_inventory(product, quantity)
    if not inv_status:
        return jsonify({"message": "Inventory update failed"}), 500

    notify_status = send_notification(product, quantity)
    if not notify_status:
        return jsonify({"message": "Notification failed after inventory update"}), 500

    billing_status = create_invoice(product, total_cost)
    if not billing_status:
        return jsonify({"message": "Billing failed after notification"}), 500

    return jsonify({
        "message": f"Order placed successfully for {quantity} {product}",
        "status": "success"
    }), 200

# --- HOMEPAGE ---
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
