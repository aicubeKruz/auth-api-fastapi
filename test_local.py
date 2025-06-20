#!/usr/bin/env python3
"""
Script para testar as funções de autenticação localmente
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.auth import create_access_token, verify_token, verify_api_key
from app.config import API_KEY
from datetime import datetime, timedelta
import json

def test_auth_functions():
    """Testa as funções de autenticação"""
    print("🔍 Testando funções de autenticação")
    print("=" * 50)
    
    # Teste 1: Verificar API Key
    print("1. Testando verificação de API Key...")
    valid_key = verify_api_key(API_KEY)
    invalid_key = verify_api_key("chave-invalida")
    
    print(f"   API Key válida: {valid_key}")
    print(f"   API Key inválida: {invalid_key}")
    print()
    
    # Teste 2: Criar token
    print("2. Testando criação de token...")
    token_data = {
        "user_id": "test_user_123",
        "permissions": ["read", "write", "admin"],
        "type": "access_token"
    }
    
    token = create_access_token(token_data)
    print(f"   Token criado: {token[:50]}...")
    print()
    
    # Teste 3: Verificar token válido
    print("3. Testando verificação de token válido...")
    payload = verify_token(token)
    
    if payload:
        print(f"   Token válido!")
        print(f"   User ID: {payload.get('user_id')}")
        print(f"   Permissions: {payload.get('permissions')}")
        print(f"   Expira em: {datetime.utcfromtimestamp(payload.get('exp'))}")
    else:
        print("   Token inválido!")
    print()
    
    # Teste 4: Verificar token inválido
    print("4. Testando verificação de token inválido...")
    invalid_payload = verify_token("token-invalido-123")
    print(f"   Token inválido retornou: {invalid_payload}")
    print()
    
    # Teste 5: Criar token com expiração customizada
    print("5. Testando token com expiração customizada...")
    short_token = create_access_token(
        token_data, 
        expires_delta=timedelta(seconds=1)
    )
    print(f"   Token de curta duração criado: {short_token[:50]}...")
    
    # Verificar imediatamente
    short_payload = verify_token(short_token)
    if short_payload:
        print(f"   Token válido imediatamente")
        print(f"   Expira em: {datetime.utcfromtimestamp(short_payload.get('exp'))}")
    
    # Aguardar e verificar novamente
    import time
    print("   Aguardando 2 segundos...")
    time.sleep(2)
    
    expired_payload = verify_token(short_token)
    print(f"   Token após expiração: {expired_payload}")
    print()
    
    print("✅ Todos os testes de autenticação concluídos!")

def show_example_usage():
    """Mostra exemplos de uso da API"""
    print("\n📚 Exemplos de uso da API:")
    print("=" * 50)
    
    print("1. Gerar token (POST /auth/token):")
    example_request = {
        "api_key": "api-key-super-secreta-123456789",
        "user_id": "usuario123",
        "permissions": ["read", "write"]
    }
    print(f"   Request: {json.dumps(example_request, indent=2)}")
    
    print("\n2. Validar token (POST /auth/validate):")
    validate_request = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    print(f"   Request: {json.dumps(validate_request, indent=2)}")
    
    print("\n3. Usar token em endpoint protegido (GET /auth/me):")
    print("   Headers: Authorization: Bearer <token>")
    
    print("\n4. Comandos para executar a API:")
    print("   # Modo desenvolvimento:")
    print("   uvicorn app.main:app --reload")
    print("   ")
    print("   # Modo produção:")
    print("   uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("   ")
    print("   # Com Docker:")
    print("   docker-compose up --build")
    print("   ")
    print("   # Deploy GCP App Engine:")
    print("   gcloud app deploy app.yaml")
    print("   ")
    print("   # Deploy GCP Cloud Run:")
    print("   gcloud builds submit --config cloudbuild.yaml")

if __name__ == "__main__":
    test_auth_functions()
    show_example_usage()