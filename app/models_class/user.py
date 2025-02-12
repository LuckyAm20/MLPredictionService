from .balance import BalanceManager
from .history import PredictionManager, TransactionManager


class User:
    def __init__(self, user_id: int, username: str, initial_balance: float = 0.0):
        self.__user_id = user_id
        self.__username = username
        self.__balance_manager = BalanceManager(initial_balance)
        self.__transaction_history = TransactionManager()
        self.__prediction_history = PredictionManager()

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def balance_manager(self) -> BalanceManager:
        return self.__balance_manager

    @property
    def transaction_history(self) -> TransactionManager:
        return self.__transaction_history

    @property
    def prediction_history(self) -> PredictionManager:
        return self.__prediction_history
