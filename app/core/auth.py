from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.core.redis_config import get_redis
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "a069a08c1cb5956347ff4ff0a8e421671aca0684f32509e9d6555689672c2a81")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# func para criar o token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    # copia o dicionario data
    to_encode = data.copy()
    # se o expires_delta for passado, usa ele, se não, usa o padrão de 15 minutos
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # atualiza o dicionario com o tempo de expiração
    to_encode.update({"exp": expire})

    # codifica o token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # armazenar token no Redis
    redis_client = get_redis()
    user_id = str(data.get("sub"))
    redis_client.setex(
        f"user_session:{user_id}",
        int(expires_delta.total_seconds() if expires_delta else 900),
        encoded_jwt
    )
    
    return encoded_jwt

# func para verificar se o token é valido
async def get_current_user(
    # pega o token do header
    token: str = Depends(oauth2_scheme),

    # pega o banco de dados
    db: Session = Depends(get_db)
) -> User:

    # cria uma exceção de credenciais inválidas 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # tenta decodificar o token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # verifica se o token está no Redis
        redis_client = get_redis()
        stored_token = redis_client.get(f"user_session:{username}")
        if not stored_token or stored_token != token:
            raise credentials_exception

    #    se der erro na decodificação, retorna o erro
    except JWTError:
        raise credentials_exception
    
    # pega o usuario do banco de dados
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        # se o usuario não for encontrado, retorna o erro
        raise credentials_exception

    # retorna o usuario
    return user


def invalidate_token(username: str):
    """Invalida o token do usuário no Redis"""
    redis_client = get_redis()
    redis_client.delete(f"user_session:{username}") 