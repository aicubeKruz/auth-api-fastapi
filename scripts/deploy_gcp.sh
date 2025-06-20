#!/bin/bash

# Script para deploy no Google Cloud Platform

echo "🌐 Deploy da API de Autenticação no GCP"
echo "========================================"

# Verificar se gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI não encontrado!"
    echo "   Instale em: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Verificar se está autenticado
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Não está autenticado no Google Cloud!"
    echo "   Execute: gcloud auth login"
    exit 1
fi

# Obter project ID atual
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Nenhum projeto configurado!"
    echo "   Execute: gcloud config set project SEU-PROJECT-ID"
    exit 1
fi

echo "📋 Projeto atual: $PROJECT_ID"
echo ""

# Opções de deploy
echo "Escolha o método de deploy:"
echo "1) App Engine"
echo "2) Cloud Run"
echo "3) Cancelar"
echo ""

read -p "Opção [1-3]: " choice

case $choice in
    1)
        echo "🚀 Fazendo deploy no App Engine..."
        gcloud app deploy app.yaml --quiet
        echo "✅ Deploy concluído!"
        echo "🌐 URL: https://$PROJECT_ID.appspot.com"
        ;;
    2)
        echo "🚀 Fazendo deploy no Cloud Run..."
        gcloud builds submit --config cloudbuild.yaml --substitutions=_PROJECT_ID=$PROJECT_ID
        echo "✅ Deploy concluído!"
        echo "🌐 URL será mostrada após o deploy"
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
echo "📖 Endpoints disponíveis:"
echo "   GET  /health        - Health check"
echo "   POST /auth/token    - Gerar token"
echo "   POST /auth/validate - Validar token"
echo "   GET  /auth/me       - Info do usuário"
echo "   GET  /docs          - Documentação Swagger"