import json
from datetime import datetime
from typing import List, Optional, Any

from sqlalchemy import DateTime, func, Integer, ForeignKey, String, Column, Boolean, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    summary: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)

    # 0 - not done
    # 1 - completed
    # 2 - failed
    # int is fine, admin can add more states
    # default 0 means if-statements check for activity
    state: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def as_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "description": self.description,
            "state": self.state,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat()
        }
