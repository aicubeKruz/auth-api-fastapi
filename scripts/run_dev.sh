#!/bin/bash

# Script para executar a aplicação em modo desenvolvimento

echo "🚀 Iniciando API de Autenticação em modo desenvolvimento..."

# Verificar se as dependências estão instaladas
if ! command -v uvicorn &> /dev/null; then
    echo "❌ uvicorn não encontrado. Instalando dependências..."
    pip install -r requirements.txt
fi

# Executar a aplicação
echo "📡 Iniciando servidor em http://localhost:8000"
echo "📖 Documentação disponível em:"
echo "   • Swagger UI: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Para parar o servidor, pressione Ctrl+C"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000