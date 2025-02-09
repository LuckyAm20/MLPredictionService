from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_session
from database.models.user import User
from services.crud.user import create_user, get_user_by_username, get_all_users
from services.crud.user import get_user_by_id, update_user_balance, update_user_model
import bcrypt

from services.crud.transaction import create_transaction

user_router = APIRouter(tags=["User"])


class UserCreate(BaseModel):
    username: str
    password: str


class ModelSelect(BaseModel):
    user_id: int
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

    return {"message": "Регистрация успешна",
            "user_id": user.id
            }


@user_router.post("/signin")
async def signin(data: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_username(data.username, session)
    if not user or not bcrypt.checkpw(data.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверные учетные данные")

    return {"message": "Авторизация успешна",
            "user_id": user.id}


@user_router.get("/balance/{user_id}")
async def get_balance(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return {"balance": user.balance}


class BalanceTopUpRequest(BaseModel):
    user_id: int
    amount: float


@user_router.post("/balance/deposit")
async def deposit_balance(data: BalanceTopUpRequest, session: Session = Depends(get_session)):
    update_user_balance(data.user_id, data.amount, session)
    transaction = create_transaction(user_id=data.user_id, amount=data.amount, session=session)
    user = get_user_by_id(data.user_id, session)
    return {
        "message": "Баланс успешно пополнен",
        "transaction_id": transaction.id,
        "new_balance": user.balance
    }


@user_router.post("/select_model")
async def select_model(data: ModelSelect, session: Session = Depends(get_session)):
    user = get_user_by_id(data.user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    available_models = ["resnet50"]
    if data.model not in available_models:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Выбранной модели не существует")

    update_user_model(user, data.model, session)
    return {"message": f"Вы выбрали модель {data.model}"}
