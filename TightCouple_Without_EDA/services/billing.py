from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.get_json()
    product = data.get('product')
    total_cost = data.get('total_cost')
    print(f"[BILLING] Created invoice for {total_cost}")
    return jsonify({"status": "success", "message": f"Invoice created for {product}"}), 200

if __name__ == "__main__":
    app.run(port=5003)
