from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime
import datetime

Base = declarative_base()

class ReinasResult(Base):
    __tablename__ = 'reinas_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    N = Column(Integer, nullable=False)
    resuelto = Column(Boolean, nullable=False)
    pasos = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

