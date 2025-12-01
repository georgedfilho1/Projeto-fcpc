import os
import redis
import psycopg2
from flask import Flask

app = Flask(__name__)

# Configuração via Variáveis de Ambiente
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')

# Conexão com Redis (Cache)
cache = redis.Redis(host=REDIS_HOST, port=6379)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return "Conectado ao PostgreSQL com sucesso!"
    except Exception as e:
        return f"Falha ao conectar no DB: {str(e)}"

@app.route('/')
def hello():
    # Incrementa contador no Redis
    count = cache.incr('hits')
    
    # Testa conexão com Banco de Dados
    db_status = get_db_connection()
    
    return f"""
    <h1>Docker Compose Orchestration Demo</h1>
    <p><b>Cache (Redis):</b> Esta página foi vista {count} vezes.</p>
    <p><b>Database (Postgres):</b> {db_status}</p>
    <p><b>Hostname:</b> {os.getenv('HOSTNAME')}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)