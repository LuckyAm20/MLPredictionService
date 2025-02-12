import json

import pika
from services.crud.prediction import create_prediction

RABBITMQ_HOST = "rabbitmq"


def publish_prediction_task(user, image_path: str, model_name: str, cost: float, prediction_id, session):
    task_data = {
        "task_id": prediction_id,
        "user_id": user.id,
        "username": user.username,
        "balance": user.balance,
        "image_path": image_path,
        "model_name": model_name,
        "cost": cost
    }

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue="ml_tasks", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="ml_tasks",
        body=json.dumps(task_data),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
    print(f"[x] Задача предсказания отправлена: {task_data}")

    create_prediction(
        user_id=user.id,
        model=task_data["model_name"],
        image_path=task_data["image_path"],
        result='',
        cost=task_data["cost"],
        session=session
    )
