# 🔐 API de Autenticação e Autorização

Sistema simples e eficiente para autenticação e autorização de APIs usando **FastAPI** e **JWT tokens**.

## ✨ Funcionalidades

- 🔑 **Geração de Tokens JWT**: Gera tokens temporários com expiração configurável
- ✅ **Validação de Tokens**: Valida se um token é válido e não expirou
- 🔒 **Autorização por API Key**: Controla quem pode gerar tokens
- 🛡️ **Endpoints Protegidos**: Exemplo de como proteger endpoints com JWT
- ☁️ **Deploy GCP Ready**: Configurado para deploy no Google Cloud Platform
- 📚 **Documentação Automática**: Swagger UI e ReDoc integrados
- 🧪 **Testes Incluídos**: Scripts de teste e demonstração
- 🐳 **Docker Ready**: Containerização com Docker e Docker Compose

## 🚀 Início Rápido

1. **Clone e configure o projeto:**
```bash
git clone <seu-repositorio>
cd auth-api
pip install -r requirements.txt
```

2. **Execute a aplicação:**
```bash
./scripts/run_dev.sh
# OU
uvicorn app.main:app --reload
```

3. **Teste a API:**
```bash
python demo_fastapi.py
```

4. **Acesse a documentação:**
- 📊 **Swagger UI**: http://localhost:8000/docs
- 📘 **ReDoc**: http://localhost:8000/redoc

## 📁 Estrutura do Projeto

```
auth-api/
├── app/                    # 📦 Código da aplicação
│   ├── __init__.py
│   ├── main.py            # 🚀 Aplicação principal FastAPI
│   ├── config.py          # ⚙️ Configurações
│   ├── models.py          # 📝 Modelos Pydantic
│   └── auth.py            # 🔐 Funções de autenticação
├── scripts/               # 🛠️ Scripts utilitários
│   ├── run_dev.sh         # 🏃 Executar em desenvolvimento
│   ├── deploy_gcp.sh      # ☁️ Deploy no GCP
│   └── test_api.sh        # 🧪 Testes da API
├── requirements.txt       # 📋 Dependências Python
├── Dockerfile            # 🐳 Configuração Docker
├── docker-compose.yml    # 🐳 Docker Compose
├── app.yaml             # ☁️ Google App Engine
├── cloudbuild.yaml      # ☁️ Cloud Build
├── demo_fastapi.py      # 🎯 Demonstração FastAPI
├── client_example.py    # 📱 Exemplo de cliente
├── test_local.py        # 🧪 Testes locais
├── .env                 # 🔒 Variáveis de ambiente
└── README.md            # 📖 Documentação
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` ou configure as seguintes variáveis:

```env
SECRET_KEY=sua-chave-secreta-super-secreta-aqui-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_KEY=api-key-super-secreta-123456789
```

## 🏃‍♂️ Como Executar

### 🐍 Localmente com Python

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn app.main:app --reload

# OU usar o script
./scripts/run_dev.sh
```

### 🐳 Com Docker

```bash
# Build e run
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

### 🧪 Executar Testes

```bash
# Testes das funções de autenticação
python test_local.py

# Demonstração da API
python demo_fastapi.py

# Exemplo de cliente
python client_example.py

# Testes completos da API (requer API rodando)
./scripts/test_api.sh
```

### ☁️ Deploy no Google Cloud Platform

```bash
# Usar o script de deploy
./scripts/deploy_gcp.sh

# OU manualmente:

# Opção 1: App Engine
gcloud app deploy app.yaml

# Opção 2: Cloud Run
gcloud builds submit --config cloudbuild.yaml
```

## 📖 Documentação da API

Após executar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints

### POST /auth/token
Gera um novo token JWT.

**Request:**
```json
{
    "api_key": "api-key-super-secreta-123456789",
    "user_id": "usuario123",
    "permissions": ["read", "write"]
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "expires_at": "2025-06-19T15:30:00"
}
```

### POST /auth/validate
Valida se um token é válido.

**Request:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
    "valid": true,
    "user_id": "usuario123",
    "permissions": ["read", "write"],
    "expires_at": "2025-06-19T15:30:00",
    "message": "Token válido"
}
```

### GET /auth/me
Endpoint protegido que retorna informações do usuário atual.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "user_id": "usuario123",
    "permissions": ["read", "write"],
    "token_type": "access_token",
    "expires_at": "2025-06-19T15:30:00"
}
```

### GET /health
Health check do serviço.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-06-19T14:00:00",
    "service": "auth-api",
    "version": "1.0.0"
}
```

## 🧪 Testes

Execute o script de testes:

```bash
python test_api.py
```

## 🔐 Segurança

- **JWT Tokens**: Tokens assinados com chave secreta
- **Expiração**: Tokens com tempo de vida limitado
- **API Key**: Controle de acesso para geração de tokens
- **Validação**: Verificação de assinatura e expiração

## 🚀 Deploy no GCP

### Pré-requisitos

1. Conta Google Cloud Platform
2. Google Cloud CLI instalado
3. Projeto GCP criado

### Passos para Deploy

1. **Configurar projeto:**
```bash
gcloud config set project SEU-PROJECT-ID
```

2. **Deploy com App Engine:**
```bash
gcloud app deploy app.yaml
```

3. **Deploy com Cloud Run:**
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Configuração de Variáveis de Ambiente no GCP

No arquivo `app.yaml` ou `cloudbuild.yaml`, ajuste as variáveis:

```yaml
env_variables:
  SECRET_KEY: "SUA-CHAVE-SECRETA-SUPER-FORTE"
  API_KEY: "SUA-API-KEY-SUPER-SECRETA"
```

## 📝 Exemplo de Uso

```python
import requests

# 1. Gerar token
response = requests.post("https://sua-api.app/auth/token", json={
    "api_key": "sua-api-key",
    "user_id": "usuario123",
    "permissions": ["read", "write"]
})

token = response.json()["access_token"]

# 2. Usar token em requisições
headers = {"Authorization": f"Bearer {token}"}
user_info = requests.get("https://sua-api.app/auth/me", headers=headers)

# 3. Validar token
validation = requests.post("https://sua-api.app/auth/validate", json={
    "token": token
})
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.