from pydantic import BaseModel
from typing import Optional, List
from model.Cliente import Cliente
from datetime import date,datetime

class ClienteSchema(BaseModel):
    """ Cadastra um novo cliente na base de dados
    """
    cpf: str 
    nome: str 
    data_nascimento: date 
    email: str 
    cep: str

class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado após seu cadastro
    """
    cpf: int = 14773253797
    nome: str = "Leonardo de Magalhaes Lecques"
    data_nascimento: date = date(1995, 5, 20)
    email: str = "leonardolecques@hotmail.com" 
    data_insercao: date = datetime.now()
    cep: str = 20551040
    estado: str = "RJ"
    bairro: str = "Vila Isabel"
    rua: str = "Hipolito da costa"
    id: int = 1

def apresenta_cliente_cadastrado(cliente):
    """ Retorna uma representação do Cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = {
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "data_nascimento": cliente.data_nascimento,
        "cep": cliente.cep,
        "estado": cliente.estado,
        "bairro": cliente.bairro,
        "rua": cliente.rua,
        "data_insercao": cliente.data_insercao,
        "email": cliente.email,
        "data_insercao": cliente.data_insercao,
        "id": cliente.id
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
    