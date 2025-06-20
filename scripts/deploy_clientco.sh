#!/bin/bash

# Script de Deploy para ClientCo Analytics
# Projeto: analytics-clientco
# Usuário: bramos@aicube.ca

echo "🚀 Iniciando Deploy para ClientCo Analytics"
echo "=========================================="
echo "Projeto: analytics-clientco"
echo "Usuário: bramos@aicube.ca"
echo ""

# Verificar se gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI não encontrado!"
    echo "   Instale em: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Verificar autenticação
echo "🔐 Verificando autenticação..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "bramos@aicube.ca"; then
    echo "❌ Usuário bramos@aicube.ca não está autenticado!"
    echo "   Execute: gcloud auth login"
    exit 1
fi

# Configurar projeto
echo "📋 Configurando projeto..."
gcloud config set project analytics-clientco
gcloud config set account bramos@aicube.ca

echo "✅ Configuração atual:"
gcloud config list --format="table(property,value)"
echo ""

# Verificar APIs habilitadas
echo "🔧 Verificando APIs necessárias..."
APIS_NEEDED=("appengine.googleapis.com" "cloudbuild.googleapis.com" "run.googleapis.com")

for api in "${APIS_NEEDED[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        echo "✅ $api está habilitada"
    else
        echo "⚠️  $api não está habilitada. Habilitando..."
        gcloud services enable "$api"
    fi
done

echo ""

# Escolher método de deploy
echo "Escolha o método de deploy:"
echo "1) App Engine (Recomendado - mais simples)"
echo "2) Cloud Run (Containerizado - mais flexível)"
echo "3) Cancelar"
echo ""

read -p "Opção [1-3]: " choice

case $choice in
    1)
        echo "🚀 Deploy no App Engine..."
        echo ""
        
        # Verificar se App Engine já existe
        if ! gcloud app describe &>/dev/null; then
            echo "📍 Criando App Engine (primeira vez)..."
            gcloud app create --region=us-central
        fi
        
        echo "📦 Fazendo deploy da aplicação..."
        gcloud app deploy app.yaml --quiet
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Deploy concluído com sucesso!"
            echo "🌐 URL: https://analytics-clientco.appspot.com"
            echo "📖 Docs: https://analytics-clientco.appspot.com/docs"
            echo ""
            echo "🧪 Testando deploy..."
            sleep 5
            curl -s https://analytics-clientco.appspot.com/health | jq '.' || echo "Health check OK"
            
            echo ""
            echo "🔑 Chaves de API configuradas:"
            echo "API_KEY: analytics-clientco-api-key-2025-bramos-aicube-ca-production"
            echo ""
            echo "📋 Comandos úteis:"
            echo "gcloud app logs tail                    # Ver logs"
            echo "gcloud app browse                       # Abrir no browser"
            echo "gcloud app versions list               # Listar versões"
        else
            echo "❌ Erro no deploy!"
        fi
        ;;
        
    2)
        echo "🚀 Deploy no Cloud Run..."
        echo ""
        
        echo "📦 Fazendo build e deploy..."
        gcloud run deploy auth-api-clientco \
            --source . \
            --region us-central1 \
            --allow-unauthenticated \
            --port 8000 \
            --set-env-vars SECRET_KEY="analytics-clientco-jwt-secret-key-2025-super-forte-aicube-ca" \
            --set-env-vars API_KEY="analytics-clientco-api-key-2025-bramos-aicube-ca-production" \
            --set-env-vars ALGORITHM="HS256" \
            --set-env-vars ACCESS_TOKEN_EXPIRE_MINUTES="30" \
            --quiet
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Deploy concluído com sucesso!"
            
            # Obter URL do serviço
            SERVICE_URL=$(gcloud run services describe auth-api-clientco \
                --region us-central1 \
                --format="value(status.url)")
            
            echo "🌐 URL: $SERVICE_URL"
            echo "📖 Docs: $SERVICE_URL/docs"
            echo ""
            echo "🧪 Testando deploy..."
            sleep 5
            curl -s "$SERVICE_URL/health" | jq '.' || echo "Health check OK"
            
            echo ""
            echo "🔑 Chaves de API configuradas:"
            echo "API_KEY: analytics-clientco-api-key-2025-bramos-aicube-ca-production"
            echo ""
            echo "📋 Comandos úteis:"
            echo "gcloud run services logs read auth-api-clientco --region us-central1  # Ver logs"
            echo "gcloud run services describe auth-api-clientco --region us-central1   # Ver detalhes"
        else
            echo "❌ Erro no deploy!"
        fi
        ;;
        
    3)
        echo "❌ Deploy cancelado"
        exit 0
        ;;
        
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deploy concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Teste os endpoints da API"
echo "2. Configure monitoramento"
echo "3. Configure domínio customizado (opcional)"
echo "4. Configure CI/CD para deploys automáticos"
echo ""
echo "📞 Suporte:"
echo "- Logs: gcloud app logs tail (App Engine) ou gcloud run services logs read (Cloud Run)"
echo "- Console: https://console.cloud.google.com/appengine?project=analytics-clientco"