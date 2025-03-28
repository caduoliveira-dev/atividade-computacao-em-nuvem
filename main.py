from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users
from app.database.database import engine, Base
from app.models import user
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Função para esperar o banco de dados estar pronto
def wait_for_db():
    max_retries = 5
    retry_interval = 5  # segundos

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname="app",
                user="postgres",
                password="root",
                host="db"
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            if i < max_retries - 1:
                time.sleep(retry_interval)
                continue
            raise

# Esperar o banco de dados estar pronto
wait_for_db()

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API RESTful",
    description="API RESTful com FastAPI",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API RESTful com FastAPI"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 