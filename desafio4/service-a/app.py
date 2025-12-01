from flask import Flask, jsonify

app = Flask(__name__)

# Dados mockados (simulando um banco de dados)
users_db = [
    {"id": 1, "name": "Alice Silva", "active_since": "2023-01-15", "role": "Admin"},
    {"id": 2, "name": "Bob Santos", "active_since": "2023-03-10", "role": "Editor"},
    {"id": 3, "name": "Carol Dias", "active_since": "2023-05-22", "role": "Viewer"}
]

@app.route('/users', methods=['GET'])
def get_users():
    """Retorna a lista de usuários em formato JSON"""
    return jsonify(users_db)

if __name__ == '__main__':
    # Roda na porta 5000 interna do container
    app.run(host='0.0.0.0', port=5000)