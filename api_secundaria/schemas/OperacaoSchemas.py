from pydantic import BaseModel
from typing import Optional, List
from model.Operacao import Operacao
from model.Cotacao import Cotacao
from datetime import datetime

class OperacaoSchema(BaseModel):
    """ Cadastra uma nova operacao na base de dados
    """
    id_cotacao: int
    data_liquidacao: str

class OperacaoViewSchema(BaseModel):
    """ Define como uma operacao será retornada após seu cadastro
    """
    id_operacao: int = 1
    id_cotacao: int = 1
    data_liquidacao: str = "D0"
    data_insercao: datetime = '2025-03-26 23:29:08'

def apresenta_operacao(Operacao):
    """ Retorna uma representação da Operacao seguindo o schema definido em
        CotacaoViewSchema.
    """
    result = {
        "id_operacao": Operacao.id_operacao,
        "id_cotacao": Operacao.id_cotacao,
        "data_liquidacao": Operacao.data_liquidacao,
        "data_insercao": Operacao.data_insercao,
    }
    return result

class OperacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será
        feita apenas com base no id da operação.
    """
    id_operacao: int = 1

class OperacaoCadastradaViewSchema (BaseModel):
    """ Define como uma operacao será retornada após seu cadastro
    """
    id_operacao: int = 1
    id_cotacao: int = 1
    data_liquidacao_operacao: str = "D0"
    data_insercao_operacao: datetime = '2025-03-26 23:29:08'
    cod_moeda_entrada: str = "BRL"
    cod_moeda_saida: str = "USD"
    descricao: str = ""
    valor_venda:  float = 5.7343
    valor_venda_d0: float = 5.7383
    valor_venda_d1: float = 5.7373
    valor_venda_d2: float = 5.7363
    data_cotacao: datetime = '2025-03-26 23:28:50'
    data_validade_cotacao: datetime = '2025-03-26 23:29:50'



def apresenta_operacao_cadastrada(Operacao, Cotacao):
    """ Retorna uma representação do Cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = {
        "id_operacao": Operacao.id_operacao,
        "id_cotacao": Operacao.id_cotacao,
        "data_liquidacao_operacao": Operacao.data_liquidacao,
        "data_insercao_operacao": Operacao.data_insercao,
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

class OperacaoAtualizaSchema(BaseModel):
    """ Define a estrutura para atualização da data de liquidação de uma operação """
    id_operacao: int
    data_liquidacao_operacao: str