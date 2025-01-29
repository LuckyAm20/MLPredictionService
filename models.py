from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from enum import Enum


class MLServiceException(Exception):
    pass


class InsufficientBalanceException(MLServiceException):
    pass


class PredictionFailedException(MLServiceException):
    pass


class MLTaskFailedException(MLServiceException):
    pass


class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BalanceManager:
    def __init__(self, initial_balance: float = 0.0):
        self.__balance = initial_balance

    def get_balance(self) -> float:
        return self.__balance

    def top_up_funds(self, amount: float) -> None:
        self.__balance += amount

    def withdraw_funds(self, amount: float) -> None:
        if self.__balance < amount:
            raise InsufficientBalanceException("Недостаточно средств.")
        self.__balance -= amount


class User:
    def __init__(self, user_id: int, username: str, initial_balance: float = 0.0):
        self.__user_id = user_id
        self.__username = username
        self.__balance_manager = BalanceManager(initial_balance)
        self.__transaction_history = TransactionManager()
        self.__prediction_history = PredictionManager()

    def get_id(self) -> int:
        return self.__user_id

    def get_username(self) -> str:
        return self.__username

    def get_balance_manager(self) -> BalanceManager:
        return self.__balance_manager

    def get_transaction_history(self) -> "TransactionManager":
        return self.__transaction_history

    def get_prediction_history(self) -> "PredictionManager":
        return self.__prediction_history


class HistoryManager(ABC):
    def __init__(self):
        self._history: list[dict] = []

    @abstractmethod
    def add_entry(self, *args, **kwargs):
        pass

    def get_history(self) -> list[dict]:
        return self._history


class TransactionManager(HistoryManager):
    def add_entry(self, user: User, amount: float, timestamp: Optional[datetime] = None):
        pass


class PredictionManager(HistoryManager):
    def add_entry(self, user: User, image_path: str, result: str, cost: float, timestamp: Optional[datetime] = None):
        pass


class MLModel(ABC):
    @abstractmethod
    def predict(self, image_path: str) -> str:
        pass


class ResNet50Model(MLModel):
    def predict(self, image_path: str) -> str:
        pass


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
        pass

    def get_status(self) -> TaskStatus:
        return self.__status
