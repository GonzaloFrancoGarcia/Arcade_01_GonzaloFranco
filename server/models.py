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

from sqlalchemy import Column, String

class CaballoResult(Base):
    __tablename__ = 'caballo_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    inicio = Column(String, nullable=False)       # e.g. "A1"
    movimientos = Column(Integer, nullable=False) # número de movimientos realizados
    completado = Column(Boolean, nullable=False)  # True si cubrió todo el tablero
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

