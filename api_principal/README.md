# API Principal – MVP Câmbio

Esta API é responsável pelo **cadastro e gerenciamento de clientes**, bem como pela **intermediação das operações de câmbio**, consultando e registrando operações via API secundária.

## 📌 Funcionalidades
- Cadastro de cliente (com consumo da API ViaCEP para preenchimento de endereço)
- Consulta e remoção de clientes
- Atualização de endereço
- Cotação de câmbio via API Secundária
- Registro e consulta de operações de câmbio

## 🚀 Como executar

Ou com Docker Compose (recomendado):
```bash
docker-compose up --build
```

## 🔗 API Externa Utilizada
- **ViaCEP** – https://viacep.com.br
  - Tipo: Gratuita e pública
  - Uso: Preenchimento automático de endereço a partir do CEP

## 📂 Rotas principais

| Método | Rota            | Descrição                          |
|--------|------------------|--------------------------------------|
| POST   | /cliente         | Cadastrar cliente com CEP           |
| GET    | /cliente         | Consultar clientes                  |
| PUT    | /cliente         | Atualizar endereço do cliente       |
| DELETE | /cliente         | Remover cliente                     |
| POST   | /cotacao         | Realizar cotação via API secundária |
| POST   | /operacao        | Registrar operação                  |
| GET    | /operacao        | Consultar operação por ID           |
| PUT    | /operacao        | Atualizar operação (D1/D2)          |

## 📄 Documentação Swagger
Acesse em:
```
http://localhost:5000/openapi
```
