import redis
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração do Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Criar conexão com Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

def get_redis():
    try:
        redis_client.ping()
        return redis_client
    except redis.ConnectionError:
        raise ConnectionError("Não foi possível conectar ao Redis") 