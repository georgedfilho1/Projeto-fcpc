import requests
from flask import Flask

app = Flask(__name__)

# URL do Serviço A (usaremos o nome do container como hostname)
SERVICE_A_URL = "http://service-a:5000/users"

@app.route('/relatorio', methods=['GET'])
def generate_report():
    try:
        # Comunicação HTTP com o Serviço A
        response = requests.get(SERVICE_A_URL)
        response.raise_for_status() # Levanta erro se status != 200
        users = response.json()

        # Lógica de apresentação (Consolidação)
        output = "<h1>Relatório de Usuários Ativos</h1><ul>"
        
        for user in users:
            output += f"<li><strong>{user['name']}</strong> ({user['role']}) - Ativo desde: {user['active_since']}</li>"
        
        output += "</ul>"
        return output

    except requests.exceptions.RequestException as e:
        return f"<h1>Erro</h1><p>Não foi possível comunicar com o Serviço A: {str(e)}</p>", 503

if __name__ == '__main__':
    # Roda na porta 5001 interna para não conflitar se rodasse localmente
    app.run(host='0.0.0.0', port=5001)