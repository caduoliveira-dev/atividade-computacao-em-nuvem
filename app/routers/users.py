from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User as UserModel
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    invalidate_token
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/users", # prefixo da rota
    tags=["users"] # tags para o swagger
)

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str # herda a classe de cima e adiciona o password

class UserResponse(UserBase):
    id: int
    is_active: bool # classe para retornar dados do usuario

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str # classe para retornar o token
    token_type: str

@router.post("/", response_model=UserResponse) # rota para criar um usuario
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token) # rota para fazer login
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout") # rota para fazer logout
async def logout(current_user: UserModel = Depends(get_current_user)):
    invalidate_token(current_user.username)
    return {"message": "Logout realizado com sucesso"}

@router.get("/me", response_model=UserResponse) # rota para pegar o usuario logado
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserResponse) # rota para pegar um usuario pelo id
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user 