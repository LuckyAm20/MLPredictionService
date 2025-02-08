from sqlmodel import Session, select
from database.models.user import User
from typing import Optional


def get_all_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()


def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_username(username: str, session: Session) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()


def create_user(username: str, role: str, balance: float, session: Session) -> User:
    new_user = User(username=username, role=role, balance=balance)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def update_user_balance(user_id: int, amount: float, session: Session) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        user.balance += amount
        session.commit()
        return user
    return None


def update_user_model(user: User, model_name: str, session: Session):
    user.selected_model = model_name
    session.commit()
