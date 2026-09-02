import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Disease(Base):
    __tablename__ = "diseases"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)


class Symptom(Base):
    __tablename__ = "symptoms"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    label: Mapped[str] = mapped_column(String(180))
    affected_part: Mapped[str] = mapped_column(String(30))


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    prompt: Mapped[str] = mapped_column(Text)
    answer_type: Mapped[str] = mapped_column(String(30))
    affected_part: Mapped[str | None] = mapped_column(String(30), nullable=True)


class Rule(Base):
    __tablename__ = "rules"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("diseases.id"))
    definition: Mapped[dict[str, Any]] = mapped_column(JSON)
    weight: Mapped[float] = mapped_column(Float)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("diseases.id"))
    text: Mapped[str] = mapped_column(Text)


class DiagnosisSession(Base):
    __tablename__ = "diagnosis_sessions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(30), default="started")


class DiagnosisAnswer(Base):
    __tablename__ = "diagnosis_answers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("diagnosis_sessions.id"))
    question_id: Mapped[str] = mapped_column(String(100))
    value: Mapped[Any] = mapped_column(JSON)


class DiagnosisResult(Base):
    __tablename__ = "diagnosis_results"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("diagnosis_sessions.id"))
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

