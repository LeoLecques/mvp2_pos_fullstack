from pydantic import BaseModel

class CotacaoRequestSchema(BaseModel):
    cpf: str
    valor_op_entrada: float
    cod_moeda_entrada: str
    cod_moeda_saida: str

class OperacaoRequestSchema(BaseModel):
    cpf: str
    id_cotacao: int
    data_liquidacao: str

class ConsultaOperacaoRequestSchema(BaseModel):
    cpf: str
    id_operacao: int

class AtualizaOperacaoSchema(BaseModel):
    cpf: str
    id_operacao: int
    data_liquidacao_operacao: str
