from flask import Flask, render_template, request, jsonify
from kafka import KafkaProducer

app = Flask(__name__)

def CreateProducer():
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: str(v).encode('utf-8'))
        return producer
    except Exception as e:
        print(f"Kafka Producer Error: {e}")
        return None

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    product = data.get("product")
    quantity = data.get("item_count")
    total_cost = data.get("total_cost")

    event = {
        "product" : product,
        "quantity" : quantity,
        "total_price" : total_cost
    }

    producer_instance = KafkaProducer()
    producer_instance.send('order_created' , value = event)

    return jsonify({
        "message": f"Order placed successfully for {quantity} {product}",
        "status": "success"
    }), 200


@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
