from database.models.transaction import Transaction
from sqlmodel import Session, select


def create_transaction(user_id: int, amount: float, session: Session) -> Transaction:
    new_transaction = Transaction(user_id=user_id, amount=amount)
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)
    return new_transaction


def get_transactions_by_user(user_id: int, session: Session) -> list[Transaction]:
    return session.exec(select(Transaction).where(Transaction.user_id == user_id)).all()


def get_all_transactions(session: Session) -> list[Transaction]:
    return session.exec(select(Transaction)).all()
