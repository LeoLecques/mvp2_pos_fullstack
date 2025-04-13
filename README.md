# L² - Plataforma de Operações Cambiais

Este projeto implementa uma arquitetura baseada em microsserviços para realizar operações cambiais.

## 🧱 Estrutura

```
backend-mvp-cambio/
├── api_principal/
│   ├── app.py
│   ├── controller/
│   ├── model/
│   ├── schemas/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── api_secundaria/
│   ├── app.py
│   ├── controller/
│   ├── model/
│   ├── schemas/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── docker-compose.yml
└── README.md
```

## 🚀 Execução com Docker

```bash
docker-compose up --build
```

Acesse:
- API Principal: http://localhost:5000/openapi
- API Secundária: http://localhost:5001/openapi
