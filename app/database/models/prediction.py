from __future__ import annotations
from sqlalchemy.orm import Mapped
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    image_path: str
    result: Optional[str] = None
    status: str = Field(default="pending")
    cost: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # user: Optional[User] = Relationship(back_populates="predictions")

    def update_status(self, new_status: str):
        self.status = new_status
        self.timestamp = datetime.now(UTC)
