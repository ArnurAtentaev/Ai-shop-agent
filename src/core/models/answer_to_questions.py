from typing import List

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    questions: Mapped[str]
    question_embeddings: Mapped[list[float]] = mapped_column(VECTOR(384))

    answer: Mapped[List["AnswerToQuestion"]] = relationship(back_populates="question")


class AnswerToQuestion(Base):
    __tablename__ = "answer_to_questions"

    answer_chunks: Mapped[str]

    question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "questions.id",
            ondelete="CASCADE",
        ),
    )

    question: Mapped["Question"] = relationship(back_populates="answer")
