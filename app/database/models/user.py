from __future__ import annotations

from typing import List, Optional

import bcrypt
from sqlmodel import Field, Relationship, SQLModel

from .prediction import Prediction
from .transaction import Transaction


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="user")
    balance: float = Field(default=0.0)
    selected_model: Optional[str] = Field(default=None)

    # transactions: List["Transaction"] = Relationship(back_populates="user")
    # predictions: List["Prediction"] = Relationship(back_populates="user")

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
