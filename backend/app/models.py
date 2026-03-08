from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
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
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
