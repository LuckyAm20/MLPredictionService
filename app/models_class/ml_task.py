from typing import Optional
from .user import User
from .ml_model import MLModel
from .enums import TaskStatus


class MLTask:
    def __init__(self, user: User, id: str, image_path: str, model: MLModel, cost: float):
        self.__task_id = id
        self.__user = user
        self.__image_path = image_path
        self.__model = model
        self.__status = TaskStatus.PENDING
        self.__result: Optional[str] = None
        self.__cost = cost

    def process_task(self) -> None:
        self.__result = self.__model.predict(self.__image_path)
        self.__status = TaskStatus.COMPLETED
        self.__user.prediction_history.add_entry(self.__user, self.__image_path, self.__result, self.__cost)

    @property
    def status(self) -> TaskStatus:
        return self.__status
