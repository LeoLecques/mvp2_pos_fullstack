from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from model import Base
import requests

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("id", Integer, primary_key=True)
    cpf = Column("cpf", String(11), unique=True)
    nome = Column(String(140))
    email = Column(String(50), unique=True)
    cep = Column(String(8))
    estado = Column(String(2), nullable = True)
    bairro = Column(String(100), nullable = True)
    rua = Column(String(100), nullable = True)
    data_nascimento = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, cpf: str, nome: str, data_nascimento: str, email: str, cep: str, 
                 estado: str = None, bairro: str = None, rua: str = None):
        """Construtor da classe Cliente"""
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = self.formata_data(data_nascimento)
        self.email = email
        self.cep = cep
        self.estado = estado
        self.bairro = bairro
        self.rua = rua
        self.data_insercao = datetime.now()

    @staticmethod
    def formata_data(data_nascimento):
        """Formata data"""
        if isinstance(data_nascimento, datetime):
            return data_nascimento
        return datetime.strptime(data_nascimento, "%d/%m/%Y")
