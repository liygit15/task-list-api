from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from flask import request
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    title: Mapped[str] 
    description: Mapped[str] 
    completed_at: Mapped[datetime | None] 
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    def to_dict(self):
        result = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete(),
            # goal=self.goal.title if self.goal_id else None
        )

        if self.goal_id:
            result["goal_id"] = self.goal_id
            
        return result
    

    @classmethod
    def from_dict(cls, dict_data):
        if dict_data.get("is_complete"):
            completed_at = datetime.now()
        else:
            completed_at = None

        return cls(
            title=dict_data["title"],
            description=dict_data["description"],
            completed_at=completed_at,
            goal_id=dict_data.get("goal_id", None)
        )


    def is_complete(self):
        if  self.completed_at:
            return True
        return False

