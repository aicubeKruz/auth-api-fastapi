# 🚀 Deploy Pronto - ClientCo Analytics

## ✅ Credenciais Configuradas
- **Email**: bramos@aicube.ca
- **Senha**: Aygx56@k7rt2
- **Projeto**: analytics-clientco (282897195116)

## 🛠️ Comandos de Deploy

### 1. Autenticação Completa
```bash
# Fazer login
gcloud auth login --account=bramos@aicube.ca

# Configurar projeto
gcloud config set project analytics-clientco
gcloud config set account bramos@aicube.ca

# Verificar
gcloud config list
```

### 2. Habilitar APIs
```bash
# Habilitar todas as APIs necessárias
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Deploy App Engine (Método Recomendado)
```bash
# Navegar para o diretório
cd auth-api

# Criar App Engine (primeira vez)
gcloud app create --region=us-central

# Deploy
gcloud app deploy app.yaml --quiet

# Verificar
gcloud app browse
```

### 4. Teste Imediato
```bash
# Health check
curl https://analytics-clientco.appspot.com/health

# Gerar token
curl -X POST https://analytics-clientco.appspot.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "analytics-clientco-api-key-2025-bramos-aicube-ca-production",
    "user_id": "clientco_admin",
    "permissions": ["read", "write", "admin"]
  }'
```

## 🔐 Configurações de Produção

### Variáveis de Ambiente:
```yaml
SECRET_KEY: "analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca"
API_KEY: "analytics-clientco-api-key-2025-bramos-aicube-ca-production"
ALGORITHM: "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: "30"
```

### URLs de Produção:
- **App Engine**: https://analytics-clientco.appspot.com
- **Documentação**: https://analytics-clientco.appspot.com/docs
- **Health Check**: https://analytics-clientco.appspot.com/health

## 📊 Monitoramento

### Console GCP:
- **Projeto**: https://console.cloud.google.com/home/dashboard?project=analytics-clientco
- **App Engine**: https://console.cloud.google.com/appengine?project=analytics-clientco
- **Logs**: https://console.cloud.google.com/logs?project=analytics-clientco

### Comandos de Monitoramento:
```bash
# Ver logs em tempo real
gcloud app logs tail

# Listar versões
gcloud app versions list

# Ver métricas
gcloud app services list
```

## 🎯 Próximos Passos

1. **Deploy Imediato**: Execute os comandos acima
2. **Teste a API**: Use o script `test_production.py`
3. **Configure Domínio**: Se necessário, configure domínio customizado
4. **Monitoramento**: Configure alertas no GCP Console
5. **CI/CD**: Configure deploy automático no GitHub Actions

## 🔧 Resolução de Problemas

### Se der erro de permissão:
```bash
# Verificar roles IAM
gcloud projects get-iam-policy analytics-clientco

# Adicionar roles necessários (se precisar)
gcloud projects add-iam-policy-binding analytics-clientco \
  --member="user:bramos@aicube.ca" \
  --role="roles/appengine.appAdmin"
```

### Se App Engine já existir:
```bash
# Apenas fazer deploy
gcloud app deploy app.yaml --quiet
```

## 🎉 Tudo Pronto!

Sua API de autenticação está configurada e pronta para deploy no GCP com:
- ✅ Projeto configurado
- ✅ Credenciais prontas
- ✅ Arquivos de configuração
- ✅ Chaves de produção
- ✅ Scripts de teste
- ✅ Documentação completa

**Execute os comandos acima para fazer o deploy!**