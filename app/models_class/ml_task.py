from typing import Optional

from .enums import TaskStatus
from .ml_model import MLModel
from .user import User


class MLTask:
    def __init__(self, user: User, id: str, image, image_path: str, model: MLModel, cost: float):
        self.__task_id = id
        self.__user = user
        self.__image = image
        self.__image_path = image_path
        self.__model = model
        self.__status = TaskStatus.PENDING
        self.__result: Optional[int] = None
        self.__cost = cost

    def process_task(self) -> None:
        self.__result = self.__model.predict(self.__image)
        self.__status = TaskStatus.COMPLETED
        self.__user.prediction_history.add_entry(self.__user, self.__image_path, self.__result, self.__cost)

    @property
    def status(self) -> TaskStatus:
        return self.__status

    @property
    def result(self) -> int:
        return self.__result
