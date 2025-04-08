from services.crud.transaction import create_transaction
from services.crud.user import (create_user, get_user_by_username,
                                update_user_balance)


def test_create_user(db_session):
    user = create_user(username="testuser", password='testpassword', role="user", balance=100.0, session=db_session)

    assert user is not None
    assert user.username == "testuser"

    user_in_db = get_user_by_username("testuser", db_session)
    assert user_in_db is not None
    assert user_in_db.username == "testuser"


def test_update_user_balance(db_session):
    user = create_user(username="testuser", password='testpassword', role="user", balance=100.0, session=db_session)
    update_user_balance(user.id, 100, db_session)

    updated_user = get_user_by_username("testuser", db_session)
    assert updated_user.balance == 200


def test_create_transaction(db_session):
    user = create_user(username="testuser", password='testpassword', role="user", balance=100.0, session=db_session)
    transaction = create_transaction(user_id=user.id, amount=50, session=db_session)

    assert transaction is not None
    assert transaction.amount == 50
    assert transaction.user_id == user.id
