from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from flask import request

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    title:Mapped[str] 
    description:Mapped[str] 
    completed_at:Mapped[datetime | None] 

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete()
        )
    

    @classmethod
    def from_dict(cls, dict_data):
        if dict_data.get("is_complete"):
            completed_at = datetime.now()
        completed_at = None
        return cls(
            title=dict_data["title"],
            description=dict_data["description"],
            completed_at=completed_at
        )

    # @staticmethod
    # def from_dict(data):
    #     return Task(
    #         id=data["id"],
    #         title=data["title"],
    #         description=data["description"],
    #         completed_at=data.get("completed_at")
    #     )


    def is_complete(self):
        if  self.completed_at:
            return True
        return False

