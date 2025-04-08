from database.database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from services.auth import get_current_user_api
from services.crud.transaction import get_transactions_by_user
from sqlalchemy.orm import Session

transaction_router = APIRouter(tags=["Transaction"])


@transaction_router.get("/history")
async def transaction_history(session: Session = Depends(get_session), user=Depends(get_current_user_api)):
    transactions = get_transactions_by_user(user.id, session)
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="История транзакций пуста")

    return transactions
