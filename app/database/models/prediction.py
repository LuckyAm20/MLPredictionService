from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    selected_model: Optional[str] = Field(default=None)
    image_path: str
    result: Optional[str] = None
    status: str = Field(default="pending")
    cost: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # user: Optional[User] = Relationship(back_populates="predictions")

    def update_status(self, new_status: str):
        self.status = new_status
        self.timestamp = datetime.now(UTC)

    def update_result(self, new_result: str):
        self.result = new_result
        self.timestamp = datetime.now(UTC)
