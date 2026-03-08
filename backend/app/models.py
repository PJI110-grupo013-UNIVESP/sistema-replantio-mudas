from sqlalchemy import Column, Integer, String
from .database import Base


class Muda(Base):
    __tablename__ = "mudas"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, index=True)
    batch = Column(String, index=True)
    supplier = Column(String)
    amount = Column(Integer)
