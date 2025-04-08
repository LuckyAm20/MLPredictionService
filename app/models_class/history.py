from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class HistoryManager(ABC):
    def __init__(self):
        self._history: list[dict] = []

    @abstractmethod
    def add_entry(self, *args, **kwargs):
        pass

    @property
    def history(self) -> list[dict]:
        return self._history


class TransactionManager(HistoryManager):
    def add_entry(self, user, amount: float, timestamp: Optional[datetime] = None):
        self._history.append({
            "user": user.username,
            "amount": amount,
            "timestamp": timestamp or datetime.now()
        })


class PredictionManager(HistoryManager):
    def add_entry(self, user, image_path: str, result: int, cost: float, timestamp: Optional[datetime] = None):
        self._history.append({
            "user": user.username,
            "image_path": image_path,
            "result": result,
            "cost": cost,
            "timestamp": timestamp or datetime.now()
        })
