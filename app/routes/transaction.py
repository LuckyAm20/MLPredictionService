from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_session
from services.crud.transaction import get_transactions_by_user

transaction_router = APIRouter(tags=["Transaction"])


@transaction_router.get("/history/{user_id}")
async def transaction_history(user_id: int, session: Session = Depends(get_session)):
    transactions = get_transactions_by_user(user_id, session)
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="История транзакций пуста")

    return transactions
