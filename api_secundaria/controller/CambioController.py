from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
import requests
from datetime import datetime, timedelta, timezone

from model import Session
from model.Cotacao import *
from model.Operacao import *
from schemas.CotacaoSchemas import *
from schemas.OperacaoSchemas import *
from schemas.erroSchemas import ErrorSchema
from flask_cors import CORS

info = Info(title="L² - OP CAMBIAL", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#Definir tags para Swagger
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cotacao_tag = Tag(name="Cotacao", description="")
operacao_tag = Tag(name="Operacao", description="")

@app.get("/", tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#Rota para realizar uma nova cotação de moeda consultando a API AWESOMEAPI
@app.post('/cotacao', tags=[cotacao_tag], responses={"200": CotacaoViewSchema,"401": ErrorSchema})
def cadastra_cotacao(body: CotacaoSchema):
    """Realizar Cadastro da Cotacao no Banco de Dados. Consulta cotacao na AWESOMEAPI"""
    try:
        form_data = request.json

        # Converte o JSON para o schema Pydantic
        form = CotacaoSchema(**form_data)

        # Consultar API da AWESOMEAPI
        url = 'https://economia.awesomeapi.com.br/json/last/{}-{}'.format(form.cod_moeda_entrada,form.cod_moeda_saida)
        headers = {'x-api-key': 'eb881ad72b60f0100c3bcc285b744ad2ec61fd664a74551a949fc1aefb073aa9'}
        consulta_cotacao = requests.get(url, headers=headers)
        
        cotacao = consulta_cotacao.json()[form.cod_moeda_entrada+form.cod_moeda_saida]
        zone_brasilia = timezone(timedelta(hours=-3))
        data_cotacao = datetime.now(zone_brasilia)
        data_validade_cotacao = data_cotacao + timedelta(seconds=60)

        # Instância da cotação
        cotacao = Cotacao(
            cod_moeda_entrada = cotacao["code"],
            cod_moeda_saida = cotacao["codein"],
            descricao = cotacao["name"],
            valor_venda = float(cotacao["ask"]),
            valor_op_d0 = round((float(cotacao["ask"]) + 0.004) * form.valor_op_entrada,2),
            valor_op_d1 = round((float(cotacao["ask"]) + 0.003) * form.valor_op_entrada,2),
            valor_op_d2 = round((float(cotacao["ask"]) + 0.002) * form.valor_op_entrada,2),
            data_cotacao = data_cotacao,
            data_validade_cotacao = data_validade_cotacao)

        session = Session()
        session.add(cotacao)
        session.commit()
        return apresenta_cotacao(cotacao), 200
    except Exception as e:
        return {"error": str(e)}, 500
    
#Rota para realizar o fechamento de uma operacao
@app.post('/operacao', tags=[operacao_tag], responses={"200": OperacaoViewSchema,"401": ErrorSchema})
def cadastra_operacao(body: OperacaoSchema):
    """Realizar Cadastro da Operacao no Banco de Dados."""
    try:
        form_data = request.json
        # Converte o JSON para o schema Pydantic
        form = OperacaoSchema(**form_data)

        # Obtém os parâmetros do contrato
        id_cotacao = form.id_cotacao
        data_liquidacao = form.data_liquidacao

        #Consulta se id_cotacao existe
        session = Session()

        valida_id_cotacao = None
        valida_id_cotacao = session.query(Cotacao).filter(Cotacao.id_cotacao == id_cotacao).first()

        if not valida_id_cotacao:
            return {"message": "id_cotacao não encontrado na base."}, 404
        
        # Certifica-se de que a data_validade_cotacao é offset-aware
        zone_brasilia = timezone(timedelta(hours=-3))
        if valida_id_cotacao.data_validade_cotacao.tzinfo is None:
            valida_id_cotacao.data_validade_cotacao = valida_id_cotacao.data_validade_cotacao.replace(tzinfo=zone_brasilia)

        # Data/hora atual em UTC
        now_utc = datetime.now(zone_brasilia)
        # Verifica se a data atual é menor que a data de validade da cotação
        if now_utc > valida_id_cotacao.data_validade_cotacao:
            return {"message": "Cotação expirada."}, 400
        
        # Instância da cotação
        operacao = Operacao(
        id_cotacao = id_cotacao,
        data_liquidacao = data_liquidacao,
        data_insercao = now_utc
        )

        session = Session()
        session.add(operacao)
        session.commit()
        return apresenta_operacao(operacao), 200
    except Exception as e:
        return {"error": str(e)}, 500

#Rota para consultar um cliente
@app.get('/operacao', tags=[operacao_tag], responses={"200": OperacaoCadastradaViewSchema, "404": ErrorSchema})
def consulta_operacao(query: OperacaoBuscaSchema):
    """Faz a busca por uma operação a partir do id_operacao"""
    try:
        session = Session()
        id_operacao = query.id_operacao

        operacao = session.query(Operacao).filter(Operacao.id_operacao == id_operacao).first()
        if not operacao:
            return {"mesage": "Operação não encontrada na base."}, 404

        cotacao = session.query(Cotacao).filter(Cotacao.id_cotacao == operacao.id_cotacao).first()
        if not cotacao:
            return {"mesage": "Cotação associada à operação não encontrada."}, 404

        return apresenta_operacao_cadastrada(operacao, cotacao), 200

    except Exception as e:
        return {"mesage": str(e)}, 500
    

@app.put('/operacao', tags=[operacao_tag], responses={"200": OperacaoViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def atualizar_operacao(body: OperacaoAtualizaSchema):
    """Atualiza a data de liquidação de uma operação, com base em regras de negócio."""
    try:
        form_data = request.json
        form = OperacaoAtualizaSchema(**form_data)

        id_operacao = form.id_operacao
        nova_data = form.data_liquidacao_operacao.upper()

        session = Session()

        operacao = session.query(Operacao).filter(Operacao.id_operacao == id_operacao).first()
        if not operacao:
            return {"message": "Operação não encontrada."}, 404

        data_insercao = operacao.data_insercao.date()
        data_hoje = datetime.now().date()

        # Regras de atualização
        if operacao.data_liquidacao == "D0":
            return {"message": "Operações D0 não podem ser atualizadas."}, 400

        if nova_data == "D0":
            return {"message": "Não é permitido atualizar uma operação para D0."}, 400

        if operacao.data_liquidacao == "D1":
            if nova_data != "D2":
                return {"message": "D1 só pode ser atualizada para D2."}, 400
            if data_insercao != data_hoje:
                return {"message": "Atualização para D2 só é permitida no mesmo dia da criação."}, 400

        if operacao.data_liquidacao == "D2":
            if nova_data != "D1":
                return {"message": "D2 só pode ser atualizada para D1."}, 400
            if data_insercao != data_hoje:
                return {"message": "Atualização para D1 só é permitida no mesmo dia da criação."}, 400

        # Atualiza e salva
        operacao.data_liquidacao = nova_data
        session.commit()

        return apresenta_operacao(operacao), 200

    except Exception as e:
        return {"message": str(e)}, 500


# Inicia um servidor web Flask que permite a aplicação responder a requisições HTTP na rede
def cambio_view():
    app.run(host="0.0.0.0", port=5001, debug = True)