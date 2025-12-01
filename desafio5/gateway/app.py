import requests
from flask import Flask, jsonify

app = Flask(__name__)

# URLs internas (dentro da rede Docker)
USER_SERVICE_URL = "http://users_service:5000/users"
ORDER_SERVICE_URL = "http://orders_service:5000/orders"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API Gateway rodando!", "endpoints": ["/users", "/orders"]})

@app.route('/users', methods=['GET'])
def proxy_users():
    try:
        response = requests.get(USER_SERVICE_URL)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service Users unavailable"}), 503

@app.route('/orders', methods=['GET'])
def proxy_orders():
    try:
        response = requests.get(ORDER_SERVICE_URL)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service Orders unavailable"}), 503

if __name__ == '__main__':
    # Roda na porta 8080 interna
    app.run(host='0.0.0.0', port=8080)