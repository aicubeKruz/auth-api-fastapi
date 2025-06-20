# 🚀 Guia de Deploy no Google Cloud Platform

## 🔧 Pré-requisitos

1. **Conta Google Cloud Platform**
   - Acesse: https://cloud.google.com/
   - Crie uma conta (se não tiver)
   - Ative a cobrança (necessário para deploy)

2. **Projeto GCP**
   - Crie um projeto no GCP Console
   - Anote o PROJECT_ID

## 🛠️ Configuração do gcloud CLI

### 1. Autenticação
```bash
# No seu terminal local (não aqui), execute:
gcloud auth login

# Ou use service account (para automação):
gcloud auth activate-service-account --key-file=path/to/service-account.json
```

### 2. Configurar projeto
```bash
# Definir projeto padrão
gcloud config set project SEU-PROJECT-ID

# Verificar configuração
gcloud config list
```

### 3. Habilitar APIs necessárias
```bash
# Para App Engine
gcloud services enable appengine.googleapis.com

# Para Cloud Run
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## 🚀 Opções de Deploy

### Opção 1: App Engine (Recomendado para início)

#### Vantagens:
- ✅ Configuração mais simples
- ✅ Scaling automático
- ✅ Domínio gratuito (.appspot.com)
- ✅ SSL/HTTPS automático

#### Deploy:
```bash
cd auth-api
gcloud app deploy app.yaml
```

#### Configuração (app.yaml):
```yaml
runtime: python311

env_variables:
  SECRET_KEY: "sua-chave-secreta-super-forte-aqui"
  ALGORITHM: "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
  API_KEY: "sua-api-key-super-secreta"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6
```

### Opção 2: Cloud Run

#### Vantagens:
- ✅ Containerizado
- ✅ Pay-per-use
- ✅ Scaling para zero
- ✅ Mais controle

#### Deploy:
```bash
cd auth-api

# Build e deploy em um comando
gcloud run deploy auth-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY="sua-chave-secreta" \
  --set-env-vars API_KEY="sua-api-key" \
  --set-env-vars ALGORITHM="HS256" \
  --set-env-vars ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

#### Ou usando Cloud Build:
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Opção 3: Compute Engine (Para mais controle)

#### Deploy manual:
```bash
# Criar VM
gcloud compute instances create auth-api-vm \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-micro \
  --zone us-central1-a

# SSH na VM
gcloud compute ssh auth-api-vm --zone us-central1-a

# Na VM, clonar e configurar
git clone https://github.com/aicubeKruz/auth-api-fastapi.git
cd auth-api-fastapi
pip install -r requirements.txt
# Configurar .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🔐 Gerenciamento de Secrets

### Para App Engine:
```bash
# Criar secret
echo "sua-chave-secreta" | gcloud secrets create secret-key --data-file=-

# Usar no app.yaml:
env_variables:
  SECRET_KEY: "projects/SEU-PROJECT-ID/secrets/secret-key/versions/latest"
```

### Para Cloud Run:
```bash
# Deploy com secrets
gcloud run deploy auth-api \
  --source . \
  --region us-central1 \
  --set-secrets SECRET_KEY=secret-key:latest
```

## 📊 Monitoramento

### Logs:
```bash
# App Engine
gcloud app logs tail

# Cloud Run
gcloud run services logs read auth-api --region us-central1
```

### Métricas:
- Acesse: https://console.cloud.google.com/monitoring

## 🔧 Configuração de Domínio Customizado

### App Engine:
```bash
gcloud app domain-mappings create sua-api.com
```

### Cloud Run:
```bash
gcloud run domain-mappings create \
  --service auth-api \
  --domain sua-api.com \
  --region us-central1
```

## 🚨 Comandos de Emergência

### Parar serviços:
```bash
# App Engine (não pode parar, apenas versões)
gcloud app versions stop VERSION-ID

# Cloud Run
gcloud run services update auth-api \
  --region us-central1 \
  --max-instances 0
```

### Rollback:
```bash
# App Engine
gcloud app versions migrate PREVIOUS-VERSION

# Cloud Run
gcloud run services replace service.yaml --region us-central1
```

## 💰 Controle de Custos

### Configurar alertas:
```bash
# Criar budget alert
gcloud billing budgets create \
  --billing-account BILLING-ACCOUNT-ID \
  --display-name "API Auth Budget" \
  --budget-amount 10USD
```

### Limitar instâncias:
```yaml
# app.yaml
automatic_scaling:
  max_instances: 2  # Limitar para controlar custos
```

## 🧪 Teste do Deploy

### Após deploy, teste:
```bash
# Substituir URL pelo seu endpoint
curl https://seu-projeto.appspot.com/health

# Gerar token
curl -X POST https://seu-projeto.appspot.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sua-api-key",
    "user_id": "test",
    "permissions": ["read"]
  }'
```

## 📞 Suporte

### Documentação oficial:
- App Engine: https://cloud.google.com/appengine/docs
- Cloud Run: https://cloud.google.com/run/docs
- gcloud CLI: https://cloud.google.com/sdk/gcloud

### Logs de erro comuns:
1. **"Project not found"**: Verificar PROJECT_ID
2. **"Permission denied"**: Verificar IAM roles
3. **"Service not enabled"**: Habilitar APIs necessárias
4. **"Quota exceeded"**: Verificar limites do projeto

---

## 🎯 Recomendação

**Para começar**: Use **App Engine** - é mais simples e tem menos configuração.

**Para produção**: Use **Cloud Run** - mais flexível e econômico.

**Para desenvolvimento**: Use **Compute Engine** - controle total.