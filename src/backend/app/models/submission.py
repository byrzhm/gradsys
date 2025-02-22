from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .. import db


class Submission(db.Model):
    __tablename__ = "submission_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[Optional[int]]  # nullable
    submit_time: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )  # pending/success/failed
    error_message: Mapped[Optional[str]]  # nullable

    __table_args__ = (UniqueConstraint("student_id", "submit_time"),)
