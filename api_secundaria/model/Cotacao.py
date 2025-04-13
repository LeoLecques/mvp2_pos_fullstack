from sqlalchemy import Column, String, Integer, DateTime, Float
from model import Base

class Cotacao(Base):
    __tablename__ = 'cotacao'

    id_cotacao = Column("id_cotacao", Integer, primary_key=True)
    cod_moeda_entrada = Column(String(5))
    cod_moeda_saida = Column(String(5))
    descricao = Column (String(100))
    valor_venda = Column(Float)
    valor_op_d0 = Column(Float)
    valor_op_d1 = Column(Float)
    valor_op_d2 = Column(Float)
    data_cotacao = Column(DateTime)
    data_validade_cotacao = Column (DateTime)

    def __init__(self, cod_moeda_entrada: str, cod_moeda_saida: str, descricao: str, 
                 valor_venda: str, valor_op_d0: str, valor_op_d1: str, valor_op_d2: str,
                 data_cotacao: str, data_validade_cotacao: str):
        """Construtor da classe Cotacao"""
        self.cod_moeda_entrada = cod_moeda_entrada
        self.cod_moeda_saida = cod_moeda_saida
        self.descricao = descricao
        self.valor_venda = valor_venda
        self.valor_op_d0 = valor_op_d0
        self.valor_op_d1 = valor_op_d1
        self.valor_op_d2 = valor_op_d2
        self.data_cotacao = data_cotacao
        self.data_validade_cotacao = data_validade_cotacao