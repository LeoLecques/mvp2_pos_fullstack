from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from model import Base

class Operacao(Base):
    __tablename__ = 'operacao'

    id_operacao = Column("id_operacao", Integer, primary_key=True)
    id_cotacao = Column("id_cotacao", Integer, unique=True)
    data_liquidacao = Column(String(2))
    data_insercao = Column (DateTime)

    def __init__(self, id_cotacao: int, data_liquidacao: str, data_insercao: datetime):
        """Construtor da classe Cotacao"""
        self.id_cotacao = id_cotacao
        self.data_liquidacao = data_liquidacao
        self.data_insercao = data_insercao