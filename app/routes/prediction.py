import os

from database.database import get_session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from services.crud.prediction import (create_prediction, get_model_by_id,
                                      get_next_prediction_id,
                                      get_prediction_by_id,
                                      get_predictions_by_user)
from services.crud.user import get_user_by_id, update_user_balance
from sqlalchemy.orm import Session
from workers.publisher import publish_prediction_task

prediction_router = APIRouter(tags=["Prediction"])


@prediction_router.post("/")
async def predict(user_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    user = get_model_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Модель не выбрана")

    cost = 10

    if user.balance >= cost:
        update_user_balance(user_id, -cost, session)
    else:
        raise HTTPException(status_code=404,
                            detail=f"Недостаточно средств. "
                                   f"Текущий баланс: {user.balance}, стоимость предсказания: {cost}.")

    temp_dir = "/app/temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    image_path = os.path.join(temp_dir, file.filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())

    prediction_id = get_next_prediction_id(session)
    publish_prediction_task(user, image_path, user.selected_model, cost, prediction_id, session)

    return {"message": "Задача отправлена в очередь",
            "prediction_id": prediction_id}


@prediction_router.get("/{prediction_id}")
async def get_prediction(prediction_id: int, session: Session = Depends(get_session)):
    prediction = get_prediction_by_id(prediction_id, session)
    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предсказание не найдено")

    return {
        "prediction_id": prediction.id,
        "model": prediction.selected_model,
        "image_path": prediction.image_path,
        "result": prediction.result,
        "status": prediction.status
    }


@prediction_router.get("/history/{user_id}")
async def prediction_history(user_id: int, session: Session = Depends(get_session)):
    predictions = get_predictions_by_user(user_id, session)
    if not predictions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="История предсказаний пуста")

    return predictions
