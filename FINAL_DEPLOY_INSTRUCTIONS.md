# 🚀 INSTRUÇÕES FINAIS DE DEPLOY - ClientCo Analytics

## 📋 Informações do Projeto
- **Projeto**: ClientCo Analytics
- **Project ID**: analytics-clientco
- **Project Number**: 282897195116
- **Email**: bramos@aicube.ca
- **Senha**: Aygx56@k7rt2

## 🎯 EXECUTE ESTES COMANDOS NO SEU TERMINAL LOCAL

### 1. Clone o Repositório (se ainda não fez)
```bash
git clone https://github.com/aicubeKruz/auth-api-fastapi.git
cd auth-api-fastapi
```

### 2. Instale o Google Cloud CLI (se não tiver)
```bash
# Linux/macOS
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Ou baixe de: https://cloud.google.com/sdk/docs/install
```

### 3. Autenticação no GCP
```bash
# Login no Google Cloud
gcloud auth login

# Quando abrir o browser, use:
# Email: bramos@aicube.ca
# Senha: Aygx56@k7rt2

# Configurar projeto
gcloud config set project analytics-clientco
gcloud config set account bramos@aicube.ca

# Verificar configuração
gcloud config list
```

### 4. Habilitar APIs Necessárias
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### 5. Deploy no App Engine
```bash
# Criar App Engine (primeira vez)
gcloud app create --region=us-central

# Deploy da aplicação
gcloud app deploy app.yaml

# Confirme com 'Y' quando perguntado
```

### 6. Verificar Deploy
```bash
# Abrir no browser
gcloud app browse

# Ou testar via curl
curl https://analytics-clientco.appspot.com/health
```

## 🧪 Testar a API

### Health Check
```bash
curl https://analytics-clientco.appspot.com/health
```

### Gerar Token
```bash
curl -X POST https://analytics-clientco.appspot.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "analytics-clientco-api-key-2025-bramos-aicube-ca-production",
    "user_id": "admin_clientco",
    "permissions": ["read", "write", "admin"]
  }'
```

### Validar Token (use o token do comando anterior)
```bash
curl -X POST https://analytics-clientco.appspot.com/auth/validate \
  -H "Content-Type: application/json" \
  -d '{
    "token": "SEU_TOKEN_AQUI"
  }'
```

### Endpoint Protegido
```bash
curl -X GET https://analytics-clientco.appspot.com/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📖 URLs Importantes

Após o deploy bem-sucedido:
- **API Base**: https://analytics-clientco.appspot.com
- **Documentação**: https://analytics-clientco.appspot.com/docs
- **ReDoc**: https://analytics-clientco.appspot.com/redoc
- **Health Check**: https://analytics-clientco.appspot.com/health

## 🔐 Chaves de Produção Configuradas

```
API_KEY: analytics-clientco-api-key-2025-bramos-aicube-ca-production
SECRET_KEY: analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca
```

## 📊 Monitoramento

### Console GCP:
- **Dashboard**: https://console.cloud.google.com/home/dashboard?project=analytics-clientco
- **App Engine**: https://console.cloud.google.com/appengine?project=analytics-clientco
- **Logs**: https://console.cloud.google.com/logs?project=analytics-clientco

### Comandos de Logs:
```bash
# Ver logs em tempo real
gcloud app logs tail

# Ver versões deployadas
gcloud app versions list

# Descrição do serviço
gcloud app describe
```

## 🔧 Se Houver Problemas

### Erro de Permissão:
```bash
# Verificar permissões
gcloud projects get-iam-policy analytics-clientco

# Adicionar role de App Engine Admin (se necessário)
gcloud projects add-iam-policy-binding analytics-clientco \
  --member="user:bramos@aicube.ca" \
  --role="roles/appengine.appAdmin"
```

### App Engine já existe:
```bash
# Se o App Engine já existir, apenas faça o deploy
gcloud app deploy app.yaml
```

### Testar localmente antes do deploy:
```bash
# No diretório do projeto
pip install -r requirements.txt
uvicorn app.main:app --reload

# Em outro terminal
python test_production.py
```

## 🎉 Deploy Bem-Sucedido!

Quando o deploy funcionar, você verá:
```
Deployed service [default] to [https://analytics-clientco.appspot.com]
```

Sua API estará disponível em:
**https://analytics-clientco.appspot.com**

## 📞 Próximos Passos

1. ✅ Teste todos os endpoints
2. ✅ Configure monitoramento
3. ✅ Configure alertas de erro
4. ✅ Configure domínio customizado (opcional)
5. ✅ Configure CI/CD para deploys automáticos

## 🔄 Deploy Alternativo (Cloud Run)

Se preferir usar Cloud Run:
```bash
gcloud run deploy auth-api-clientco \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars SECRET_KEY="analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca" \
  --set-env-vars API_KEY="analytics-clientco-api-key-2025-bramos-aicube-ca-production"
```

---

## ⚡ RESUMO RÁPIDO:

1. `gcloud auth login` (use bramos@aicube.ca / Aygx56@k7rt2)
2. `gcloud config set project analytics-clientco`
3. `gcloud services enable appengine.googleapis.com`
4. `gcloud app create --region=us-central`
5. `gcloud app deploy app.yaml`
6. `gcloud app browse`

**🎯 Execute estes comandos e sua API estará no ar!**