from datetime import timedelta

import bcrypt
from database.database import get_session
from database.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from services.crud.transaction import create_transaction
from services.crud.user import (create_user, get_all_users, get_user_by_id,
                                get_user_by_username, update_user_balance,
                                update_user_model)
from sqlalchemy.orm import Session

from services.auth import create_access_token, get_current_user_api

user_router = APIRouter(tags=["User"])


class UserCreate(BaseModel):
    username: str
    password: str


class ModelSelect(BaseModel):
    model: str


@user_router.post("/signup")
async def signup(data: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_username(data.username, session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")

    user = User(username=data.username)
    salt = bcrypt.gensalt()
    user.password_hash = bcrypt.hashpw(data.password.encode(), salt).decode()

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "Регистрация успешна",
        "user_id": user.id
    }


@user_router.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_username(form_data.username, session)
    if not user or not bcrypt.checkpw(form_data.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные")

    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/signin")
async def signin(data: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_username(data.username, session)
    if not user or not bcrypt.checkpw(data.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверные учетные данные")

    return {"message": "Авторизация успешна",
            "user_id": user.id}


@user_router.get("/balance")
async def get_balance(session: Session = Depends(get_session), user=Depends(get_current_user_api)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return {"balance": user.balance}


@user_router.post("/balance/deposit/{amount}")
async def deposit_balance(amount: int, session: Session = Depends(get_session), user=Depends(get_current_user_api)):
    update_user_balance(user.id, amount, session)
    transaction = create_transaction(user_id=user.id, amount=amount, session=session)
    return {
        "message": "Баланс успешно пополнен",
        "transaction_id": transaction.id,
        "new_balance": user.balance
    }


@user_router.post("/select_model")
async def select_model(data: ModelSelect, session: Session = Depends(get_session), user=Depends(get_current_user_api)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    available_models = ["resnet50"]
    if data.model not in available_models:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Выбранной модели не существует")

    update_user_model(user, data.model, session)
    return {"message": f"Вы выбрали модель {data.model}"}
