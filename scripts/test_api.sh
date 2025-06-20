#!/bin/bash

# Script para testar a API de autenticação

API_URL="http://localhost:8000"
API_KEY="api-key-super-secreta-123456789"

echo "🧪 Testando API de Autenticação"
echo "================================"
echo "URL: $API_URL"
echo ""

# Verificar se a API está rodando
echo "1. Verificando se a API está rodando..."
if curl -s "$API_URL/health" > /dev/null; then
    echo "✅ API está rodando"
else
    echo "❌ API não está rodando"
    echo "   Execute: ./scripts/run_dev.sh"
    exit 1
fi

echo ""

# Health check
echo "2. Health Check"
echo "---------------"
curl -s "$API_URL/health" | jq '.'
echo ""

# Gerar token
echo "3. Gerando token..."
echo "-------------------"
TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/auth/token" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"user_id\": \"test_user_123\",
    \"permissions\": [\"read\", \"write\", \"admin\"]
  }")

echo "$TOKEN_RESPONSE" | jq '.'

# Extrair token
TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" = "null" ]; then
    echo "❌ Falha ao gerar token"
    exit 1
fi

echo "✅ Token gerado: ${TOKEN:0:50}..."
echo ""

# Validar token
echo "4. Validando token..."
echo "---------------------"
curl -s -X POST "$API_URL/auth/validate" \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}" | jq '.'
echo ""

# Testar endpoint protegido
echo "5. Testando endpoint protegido..."
echo "---------------------------------"
curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo ""

# Testar token inválido
echo "6. Testando token inválido..."
echo "-----------------------------"
curl -s -X POST "$API_URL/auth/validate" \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"token-invalido-123\"}" | jq '.'
echo ""

# Testar API key inválida
echo "7. Testando API key inválida..."
echo "-------------------------------"
curl -s -X POST "$API_URL/auth/token" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"api-key-invalida\",
    \"user_id\": \"test_user\",
    \"permissions\": [\"read\"]
  }" | jq '.'
echo ""

echo "✅ Todos os testes concluídos!"
echo ""
echo "📖 Para ver a documentação completa:"
echo "   Swagger UI: $API_URL/docs"
echo "   ReDoc: $API_URL/redoc"