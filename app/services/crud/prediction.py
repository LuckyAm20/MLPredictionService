from sqlmodel import Session, select
from database.models.user import Prediction
from typing import Optional


def create_prediction(user_id: int, image_path: str, cost: float, session: Session) -> Prediction:
    new_prediction = Prediction(user_id=user_id, image_path=image_path, cost=cost)
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
