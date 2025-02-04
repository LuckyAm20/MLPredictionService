from models.user import User
from models.ml_model import ResNet50Model
from models.ml_task import MLTask

from database.database import init_db, get_session
from services.crud.user import create_user, get_all_users, update_user_balance
from services.crud.transaction import create_transaction, get_transactions_by_user
from services.crud.prediction import create_prediction, get_predictions_by_user


def test_database():
    init_db()
    print("База данных инициализирована")

    with get_session() as session:
        user1 = create_user(username="Misha", role="user", balance=100.0, session=session)
        user2 = create_user(username="Alex", role="admin", balance=200.0, session=session)

        print("\nПользователи созданы:")
        users = get_all_users(session)
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}, Balance: {user.balance}")

        update_user_balance(user_id=user1.id, amount=50.0, session=session)
        print(f"\nБаланс {user1.username} после пополнения: {user1.balance}")

        create_transaction(user_id=user1.id, amount=50.0, session=session)
        create_transaction(user_id=user2.id, amount=-100.0, session=session)

        print("\nТранзакции пользователя Misha:")
        transactions = get_transactions_by_user(user_id=user1.id, session=session)
        for tx in transactions:
            print(f"ID: {tx.id}, UserID: {tx.user_id}, Amount: {tx.amount}, Time: {tx.timestamp}")

        create_prediction(user_id=user1.id, image_path="dog.jpg", cost=10.0, session=session)
        create_prediction(user_id=user2.id, image_path="cat.jpg", cost=15.0, session=session)

        print("\nПредсказания пользователя Misha:")
        predictions = get_predictions_by_user(user_id=user1.id, session=session)
        for pred in predictions:
            print(
                f"ID: {pred.id}, UserID: {pred.user_id}, Image: {pred.image_path}, Cost: {pred.cost}, Status: {pred.status}")


if __name__ == '__main__':
    # user = User(user_id=1, username="misha", initial_balance=100)
    #
    # print(f"Начальный баланс: {user.balance_manager.balance}")
    #
    # model = ResNet50Model()
    #
    # task = MLTask(user, id="task1", image_path="dog.jpg", model=model, cost=10)
    #
    # task.process_task()
    #
    # print(f"Баланс после выполнения задачи: {user.balance_manager.balance}")
    #
    # print(f"Статус задачи: {task.status}")
    #
    # print("История предсказаний:", user.prediction_history.history)
    test_database()
