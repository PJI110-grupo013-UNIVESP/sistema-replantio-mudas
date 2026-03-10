from sqlalchemy import String, Boolean, ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Optional
from .database import Base


class Muda(Base):
    __tablename__ = "mudas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    species: Mapped[str] = mapped_column(String, index=True)
    batch: Mapped[str] = mapped_column(String, index=True)
    supplier: Mapped[str] = mapped_column(String)
    amount: Mapped[int] = mapped_column()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, default="Guest")
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="common")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Replantio(Base):
    __tablename__ = "replantios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    muda_id: Mapped[int] = mapped_column(ForeignKey('mudas.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    area_name: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String, default="Planejado")

    planned_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    actual_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    estimated_cost: Mapped[Optional[float]
                           ] = mapped_column(Float, nullable=True)
    actual_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    surviving_amount: Mapped[Optional[int]] = mapped_column(nullable=True)

    muda = relationship("Muda")
    user = relationship("User")
