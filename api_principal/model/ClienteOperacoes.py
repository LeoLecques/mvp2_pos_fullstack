from sqlalchemy import Column, Integer, String
from model import Base

class ClienteCotacao(Base):
    __tablename__ = "cliente_cotacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11))
    id_cotacao = Column(Integer)

class ClienteOperacao(Base):
    __tablename__ = "cliente_operacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11))
    id_operacao = Column(Integer)