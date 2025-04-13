# API Secundária – MVP Câmbio

Esta API é responsável por **realizar a cotação de câmbio** (consultando a AwesomeAPI) e **registrar operações cambiais** baseadas nas cotações válidas.

## 📌 Funcionalidades
- Consulta de cotação via AwesomeAPI
- Registro de cotações com validade de 60 segundos
- Registro de operações com base em cotação válida
- Consulta e atualização de operações

## 🚀 Como executar

Ou com Docker Compose (recomendado):
```bash
docker-compose up --build
```

## 🔗 API Externa Utilizada
- **AwesomeAPI** – https://docs.awesomeapi.com.br/api-de-moedas
  - Tipo: Gratuita e pública (com chave de API)
  - Uso: Consulta de paridades cambiais (USD-BRL, EUR-BRL, etc.)

## 📂 Rotas principais

| Método | Rota         | Descrição                             |
|--------|--------------|-----------------------------------------|
| POST   | /cotacao     | Realiza cotação com valores D0/D1/D2  |
| POST   | /operacao    | Registra uma nova operação             |
| GET    | /operacao    | Consulta uma operação por ID           |
| PUT    | /operacao    | Atualiza data de liquidação (D1↔D2)    |

## 📄 Documentação Swagger
Acesse em:
```
http://localhost:5001/openapi
```
