import json
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from database.database import get_session
from services.crud.prediction import create_prediction, get_predictions_by_user, get_model_by_id
from services.crud.user import get_user_by_id, update_user_balance
import torch
from torchvision import transforms
from PIL import Image
import io

from models_class.ml_model import MLModel

prediction_router = APIRouter(tags=["Prediction"])

models = {
}
label_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", f"imagenet-simple-labels.json")
with open(label_path) as f:
    labels = json.load(f)


def load_model(model: str):
    if model not in models:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", f"{model}.pth")
        try:
            models[model] = torch.load(model_path, weights_only=False)
            models[model].eval()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Model '{model}' not found.")
    return models[model]


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


@prediction_router.post("/")
async def predict(user_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    user = get_model_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Модель не выбрана")

    model = load_model(user.selected_model)

    ml_model = MLModel(model)

    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image = transform(image).unsqueeze(0)

    predicted_class = ml_model.predict(image)

    cost = 10

    prediction = create_prediction(user_id, user.selected_model, file.filename, labels[predicted_class], cost, session)

    if user.balance >= cost:
        update_user_balance(user_id, -cost, session)
    else:
        raise HTTPException(status_code=404,
                            detail=f"Недостаточно средств. "
                                   f"Текущий баланс: {user.balance}, стоимость предсказания: {cost}.")

    return {
        "message": "Предсказание выполнено",
        "prediction_id": prediction.id,
        "result": labels[predicted_class]
    }


@prediction_router.get("/history/{user_id}")
async def prediction_history(user_id: int, session: Session = Depends(get_session)):
    predictions = get_predictions_by_user(user_id, session)
    if not predictions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="История предсказаний пуста")

    return predictions
