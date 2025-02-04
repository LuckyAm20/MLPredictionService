from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


from .transaction import Transaction
from .prediction import Prediction


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False)
    role: str = Field(default="user")
    balance: float = Field(default=0.0)

    # transactions: List["Transaction"] = Relationship(back_populates="user")
    # predictions: List["Prediction"] = Relationship(back_populates="user")
