# 🚀 Comandos para Deploy no GCP

## ✅ Dados do Projeto Configurados
- **Project Name**: ClientCo
- **Project ID**: analytics-clientco
- **Project Number**: 282897195116
- **User**: bramos@aicube.ca

## 🔧 Passos para Deploy

### 1. Autenticação (Execute no seu terminal local)
```bash
# Fazer login no GCP
gcloud auth login

# Configurar projeto
gcloud config set project analytics-clientco
gcloud config set account bramos@aicube.ca

# Verificar configuração
gcloud config list
```

### 2. Habilitar APIs Necessárias
```bash
# Habilitar App Engine API
gcloud services enable appengine.googleapis.com

# Habilitar Cloud Build API (para Cloud Run)
gcloud services enable cloudbuild.googleapis.com

# Habilitar Cloud Run API
gcloud services enable run.googleapis.com

# Verificar APIs habilitadas
gcloud services list --enabled
```

### 3. Deploy com App Engine (Recomendado)
```bash
# Navegar para o diretório do projeto
cd path/to/auth-api

# Deploy (primeira vez - criará app)
gcloud app create --region=us-central

# Deploy da aplicação
gcloud app deploy app.yaml

# Abrir no browser
gcloud app browse
```

### 4. Alternativa: Deploy com Cloud Run
```bash
# Deploy direto do código fonte
gcloud run deploy auth-api-clientco \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY="analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca" \
  --set-env-vars API_KEY="analytics-clientco-api-key-2025-bramos-aicube-ca-production" \
  --set-env-vars ALGORITHM="HS256" \
  --set-env-vars ACCESS_TOKEN_EXPIRE_MINUTES="30" \
  --port 8000
```

### 5. Verificar Deploy
```bash
# Para App Engine
curl https://analytics-clientco.appspot.com/health

# Para Cloud Run (URL será mostrada após deploy)
curl https://CLOUD-RUN-URL/health
```

## 📋 Arquivos Preparados

### app.yaml (App Engine)
```yaml
runtime: python311

env_variables:
  SECRET_KEY: "analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca"
  ALGORITHM: "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
  API_KEY: "analytics-clientco-api-key-2025-bramos-aicube-ca-production"

automatic_scaling:
  min_instances: 1
  max_instances: 5
  target_cpu_utilization: 0.7

instance_class: F1
```

### cloudbuild.yaml (Cloud Run)
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/analytics-clientco/auth-api:$COMMIT_SHA', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/analytics-clientco/auth-api:$COMMIT_SHA']
  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
    - 'run'
    - 'deploy'
    - 'auth-api-clientco'
    - '--image'
    - 'gcr.io/analytics-clientco/auth-api:$COMMIT_SHA'
    - '--region'
    - 'us-central1'
    - '--platform'
    - 'managed'
    - '--allow-unauthenticated'
    - '--set-env-vars'
    - 'SECRET_KEY=analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca,API_KEY=analytics-clientco-api-key-2025-bramos-aicube-ca-production,ALGORITHM=HS256,ACCESS_TOKEN_EXPIRE_MINUTES=30'

images:
  - 'gcr.io/analytics-clientco/auth-api:$COMMIT_SHA'
```

## 🧪 Testes Após Deploy

### 1. Health Check
```bash
# App Engine
curl https://analytics-clientco.appspot.com/health

# Resposta esperada:
# {"status":"healthy","timestamp":"...","service":"auth-api","version":"1.0.0"}
```

### 2. Gerar Token
```bash
curl -X POST https://analytics-clientco.appspot.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "analytics-clientco-api-key-2025-bramos-aicube-ca-production",
    "user_id": "test_user_clientco",
    "permissions": ["read", "write"]
  }'
```

### 3. Validar Token
```bash
# Use o token retornado do comando anterior
curl -X POST https://analytics-clientco.appspot.com/auth/validate \
  -H "Content-Type: application/json" \
  -d '{
    "token": "SEU_TOKEN_AQUI"
  }'
```

### 4. Endpoint Protegido
```bash
curl -X GET https://analytics-clientco.appspot.com/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### 5. Documentação
```
https://analytics-clientco.appspot.com/docs
```

## 📊 Monitoramento

### Ver logs:
```bash
# App Engine
gcloud app logs tail

# Cloud Run
gcloud run services logs read auth-api-clientco --region us-central1
```

### Métricas:
- Console GCP: https://console.cloud.google.com/monitoring

## 🔐 Chaves de Produção

### Secret Key JWT:
```
analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca
```

### API Key:
```
analytics-clientco-api-key-2025-bramos-aicube-ca-production
```

## 🚨 Comandos de Emergência

### Parar App Engine:
```bash
# Listar versões
gcloud app versions list

# Parar versão específica
gcloud app versions stop VERSION-ID
```

### Atualizar configuração:
```bash
# Novo deploy
gcloud app deploy app.yaml

# Ver versões
gcloud app versions list
```

## 💡 URLs Importantes

- **App Engine Console**: https://console.cloud.google.com/appengine?project=analytics-clientco
- **Cloud Run Console**: https://console.cloud.google.com/run?project=analytics-clientco
- **API & Services**: https://console.cloud.google.com/apis?project=analytics-clientco
- **Logs**: https://console.cloud.google.com/logs?project=analytics-clientco

## 📞 Próximos Passos

1. **Execute os comandos acima no seu terminal local**
2. **Teste a API com os endpoints fornecidos**
3. **Configure domínio customizado se necessário**
4. **Configure alertas de monitoramento**
5. **Configure CI/CD para deploys automáticos**

---

🎯 **Tudo está pronto para deploy! Execute os comandos acima no seu terminal local com gcloud CLI configurado.**