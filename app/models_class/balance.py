from .exceptions import InsufficientBalanceException


class BalanceManager:
    def __init__(self, initial_balance: float = 0.0):
        self.__balance = initial_balance

    @property
    def balance(self) -> float:
        return self.__balance

    def top_up_funds(self, amount: float) -> None:
        self.__balance += amount

    def withdraw_funds(self, amount: float) -> None:
        if self.__balance < amount:
            raise InsufficientBalanceException("Недостаточно средств.")
        self.__balance -= amount
