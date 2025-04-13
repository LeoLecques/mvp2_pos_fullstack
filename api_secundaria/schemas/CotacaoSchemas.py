from pydantic import BaseModel
from typing import Optional, List
from model.Cotacao import Cotacao
from datetime import datetime

class CotacaoSchema(BaseModel):
    """ Cadastra uma nova cotacao na base de dados
    """
    valor_op_entrada: float
    cod_moeda_entrada: str
    cod_moeda_saida: str


class CotacaoViewSchema(BaseModel):
    """ Define como um cliente será retornado após seu cadastro
    """
    id_cotacao: int = 1
    cod_moeda_entrada: str = "BRL"
    cod_moeda_saida: str = "USD"
    descricao: str = "Dólar Americano/Real Brasileiro"
    valor_venda:  float = 5.7343
    valor_op_d0: float = 5.7383
    valor_op_d1: float = 5.7373
    valor_op_d2: float = 5.7363
    data_cotacao: datetime = '2025-03-26 23:29:08'
    data_validade_cotacao: datetime = '2025-03-26 23:30:08'

def apresenta_cotacao(Cotacao):
    """ Retorna uma representação da Cotacao seguindo o schema definido em
        CotacaoViewSchema.
    """
    result = {
        "id_cotacao": Cotacao.id_cotacao,
        "cod_moeda_entrada": Cotacao.cod_moeda_entrada,
        "cod_moeda_saida": Cotacao.cod_moeda_saida,
        "descricao": Cotacao.descricao,
        "valor_venda":  Cotacao.valor_venda,
        "valor_venda_d0": Cotacao.valor_op_d0,
        "valor_venda_d1": Cotacao.valor_op_d1,
        "valor_venda_d2": Cotacao.valor_op_d2,
        "data_cotacao": Cotacao.data_cotacao,
        "data_validade_cotacao": Cotacao.data_validade_cotacao
    }
    return result

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    cpf: int = 14773253797
    email: str = "leonardolecques@hotmail.com" 
    id: int = 1

class ClienteAtualizaSchema(BaseModel):
    cpf: str
    cep: str 
    estado: str 
    bairro: str 
    rua: str 

class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    cpf: str

class ClienteBuscaSchemaDel(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    cpf: int = 14773253797
    