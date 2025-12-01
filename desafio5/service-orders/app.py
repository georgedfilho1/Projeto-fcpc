from flask import Flask, jsonify

app = Flask(__name__)

orders = [
    {"id": 101, "item": "Notebook", "price": 2500, "user_id": 1},
    {"id": 102, "item": "Mouse", "price": 50, "user_id": 1}
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)