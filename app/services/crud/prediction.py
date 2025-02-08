from sqlmodel import Session, select
from database.models.user import Prediction
from typing import Optional

from database.models.user import User


def create_prediction(user_id: int, model: str, image_path: str, result: str, cost: float, session: Session) -> Prediction:
    new_prediction = Prediction(user_id=user_id, selected_model=model, image_path=image_path, result=result, cost=cost)
    session.add(new_prediction)
    session.commit()
    session.refresh(new_prediction)
    return new_prediction


def get_predictions_by_user(user_id: int, session: Session) -> list[Prediction]:
    return session.exec(select(Prediction).where(Prediction.user_id == user_id)).all()


def update_prediction_status(prediction_id: int, new_status: str, session: Session) -> Optional[Prediction]:
    prediction = session.get(Prediction, prediction_id)
    if prediction:
        prediction.update_status(new_status)
        session.commit()
        return prediction
    return None


def get_all_predictions(session: Session) -> list[Prediction]:
    return session.exec(select(Prediction)).all()


def get_model_by_id(user_id: int, session: Session) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    if user and user.selected_model:
        return user
    return None
