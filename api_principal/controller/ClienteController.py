from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
import requests

from model import Session
from model.Cliente import *
from model.ClienteOperacoes import *
from schemas.ClienteSchemas import *
from schemas.ClienteOperacoesSchema import *
from schemas.erroSchemas import ErrorSchema
from flask_cors import CORS

info = Info(title="L² - OP CAMBIAL", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#Definir tags para Swagger
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="")

@app.get("/", tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#Rota para cadastrar um novo cliente. Caso o CEP esteja registrado na VIACEP, o preenchimento será automático
@app.post('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema,"401": ErrorSchema})
def cadastra_cliente(body: ClienteSchema):
    """Realizar Cadastro de Cliente no Banco de Dados. Busca dados de endereço a partir do CEP no sistema VIACEP"""
    try:
        form_data = request.json

        # Converte o JSON para o schema Pydantic
        form = ClienteSchema(**form_data)

        # Consultar API da VIACEP
        consulta_cep = requests.get("http://viacep.com.br/ws/{}/json/".format(form.cep)).json()

        #Se não houver registro, deixa os campos de endereço como NULL
        if "erro" in consulta_cep.keys():
            # Instância do cliente com formatações
            cliente = Cliente(
                cpf=form.cpf,
                nome=form.nome,
                data_nascimento=form.data_nascimento.strftime("%d/%m/%Y"),
                email=form.email,
                cep = form.cep
            )
        #Se houver registro, preenche os campos de endereço
        else:
            cliente = Cliente(
                cpf=form.cpf,
                nome=form.nome,
                data_nascimento=form.data_nascimento.strftime("%d/%m/%Y"),
                email=form.email,
                cep = form.cep,
                estado = consulta_cep["uf"],
                bairro = consulta_cep["bairro"],
                rua = consulta_cep["logradouro"]
            )

        session = Session()
        session.add(cliente)
        session.commit()
        return apresenta_cliente_cadastrado(cliente), 200
    except Exception as e:
        return {"error": str(e)}, 500

#Rota para consultar um cliente
@app.get('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema})
def consulta_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um cliente a partir do cpf, email ou id"""
    session = Session()

    # Obtém os parâmetros da query
    email = request.args.get("email")
    cpf = request.args.get("cpf")
    id = request.args.get("id")

    cliente = None
    if cpf:
        cliente = session.query(Cliente).filter(Cliente.cpf == cpf).first()
    elif email:
        cliente = session.query(Cliente).filter(Cliente.email == email).first()
    elif id:
        cliente = session.query(Cliente).filter(Cliente.id == id).first()

    if not cliente:
        return {"message": "Cliente não encontrado na base."}, 404
    return apresenta_cliente_cadastrado(cliente), 200

#Atualiza dados de endereço de um cliente. Útil para quando um CEP não estiver registrado no VIACEP
@app.put('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema})
def atualizar_cliente(body: ClienteAtualizaSchema):
    """Atualiza as informações de endereço de um cliente a partir do CPF.

    Os campos que podem ser atualizados incluem celular, email, data de nascimento e margem.
    """
    try:
        # Converte o JSON para o schema Pydantic
        dados_atualizacao = ClienteAtualizaSchema(**request.json)

        # Cria a sessão
        session = Session()

        # Busca o cliente pelo CPF
        cliente = session.query(Cliente).filter(Cliente.cpf == dados_atualizacao.cpf).first()

        if not cliente:
            # Se o cliente não foi encontrado
            return {"message": "Cliente não encontrado na base."}, 404

        # Atualiza os campos fornecidos no body
        if dados_atualizacao.estado:
            cliente.estado = dados_atualizacao.estado
        if dados_atualizacao.bairro:
            cliente.bairro = dados_atualizacao.bairro
        if dados_atualizacao.rua:
            cliente.rua = dados_atualizacao.rua

        # Salva as alterações
        session.commit()

        # Retorna o cliente atualizado
        return apresenta_cliente_cadastrado(cliente), 200
    
    except Exception as e:
        return {"error": str(e)}, 500
    
#Deleta um cliente
@app.delete('/cliente', 
            tags=[cliente_tag],responses={"200": ClienteDelSchema})
def del_cliente(query: ClienteBuscaSchemaDel):
    """Deleta um Cliente a partir do CPF de cliente informado
    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_cpf = query.cpf
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Cliente removido", "cpf": cliente_cpf}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base."
        return {"mesage": "Cliente não econtrado na base"}, 404
    

@app.post('/cotacao', tags=[cliente_tag])
def realizar_cotacao(body: CotacaoRequestSchema):
    """ Realiza a cotação para um cliente cadastrado"""
    try:
        session = Session()

        cliente = session.query(Cliente).filter(Cliente.cpf == body.cpf).first()
        if not cliente:
            return {"message": "Cliente não encontrado."}, 404

        payload = {
            "valor_op_entrada": body.valor_op_entrada,
            "cod_moeda_entrada": body.cod_moeda_entrada,
            "cod_moeda_saida": body.cod_moeda_saida
        }

        resposta = requests.post("http://api_secundaria:5001/cotacao", json=payload)
        if resposta.status_code != 200:
            return {"message": "Erro na cotação."}, 400

        dados_cotacao = resposta.json()

        nova = ClienteCotacao(cpf=body.cpf, id_cotacao=dados_cotacao["id_cotacao"])
        session.add(nova)
        session.commit()
        return dados_cotacao, 200

    except Exception as e:
        return {"message": str(e)}, 500

@app.post('/operacao', tags=[cliente_tag])
def realizar_operacao(body: OperacaoRequestSchema):
    """Transforma uma cotação em um fechamento de operação"""
    try:
        session = Session()

        existe = session.query(ClienteCotacao).filter(
            ClienteCotacao.cpf == body.cpf,
            ClienteCotacao.id_cotacao == body.id_cotacao
        ).first()

        if not existe:
            return {"message": "Cotação não encontrada para o CPF."}, 404

        payload = {
            "id_cotacao": body.id_cotacao,
            "data_liquidacao": body.data_liquidacao
        }

        resposta = requests.post("http://api_secundaria:5001/operacao", json=payload)
        if resposta.status_code != 200:
            return {"message": "Erro ao registrar operação."}, 400

        dados_operacao = resposta.json()

        nova = ClienteOperacao(cpf=body.cpf, id_operacao=dados_operacao["id_operacao"])
        session.add(nova)
        session.commit()
        return dados_operacao, 200

    except Exception as e:
        return {"message": str(e)}, 500
    
@app.get('/operacao', tags=[cliente_tag])
def consultar_operacao(query: ConsultaOperacaoRequestSchema):
    """Realiza a consulta de uma operação"""
    try:
        session = Session()

        existe = session.query(ClienteOperacao).filter(
            ClienteOperacao.cpf == cpf,
            ClienteOperacao.id_operacao == id_operacao
        ).first()

        if not existe:
            return {"message": "Operação não encontrada para este CPF."}, 404

        resposta = requests.get("http://api_secundaria:5001/operacao", params={"id_operacao": id_operacao})
        if resposta.status_code != 200:
            return {"message": "Erro ao consultar operação."}, 400

        return resposta.json(), 200

    except Exception as e:
        return {"message": str(e)}, 500

@app.put('/operacao', tags=[cliente_tag])
def atualizar_operacao(body: AtualizaOperacaoSchema):
    """Realiza a alteração da data de liquidação de uma operação"""
    try:
        session = Session()

        existe = session.query(ClienteOperacao).filter(
            ClienteOperacao.cpf == body.cpf,
            ClienteOperacao.id_operacao == body.id_operacao
        ).first()

        if not existe:
            return {"message": "Operação não encontrada para este CPF."}, 404

        payload = {
            "id_operacao": body.id_operacao,
            "data_liquidacao_operacao": body.data_liquidacao_operacao
        }

        resposta = requests.put("http://api_secundaria:5001/operacao", json=payload)
        if resposta.status_code != 200:
            return {"message": "Erro ao atualizar operação."}, 400

        return resposta.json(), 200

    except Exception as e:
        return {"message": str(e)}, 500

    
#inicia um servidor web Flask que permite a aplicação responder a requisições HTTP na rede
def cliente_view():
    app.run(host="0.0.0.0", port=5000, debug = True)


