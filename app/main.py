from models.user import User
from models.ml_model import ResNet50Model
from models.ml_task import MLTask


if __name__ == '__main__':
    user = User(user_id=1, username="misha", initial_balance=100)

    print(f"Начальный баланс: {user.balance_manager.balance}")

    model = ResNet50Model()

    task = MLTask(user, id="task1", image_path="dog.jpg", model=model, cost=10)

    task.process_task()

    print(f"Баланс после выполнения задачи: {user.balance_manager.balance}")

    print(f"Статус задачи: {task.status}")

    print("История предсказаний:", user.prediction_history.history)
