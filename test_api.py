#!/usr/bin/env python3
"""
Script para testar a API de autenticação
"""

import requests
import json
import time
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8000"
API_KEY = "api-key-super-secreta-123456789"

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_generate_token():
    """Testa a geração de token"""
    print("🔑 Testando geração de token...")
    
    payload = {
        "api_key": API_KEY,
        "user_id": "test_user_123",
        "permissions": ["read", "write", "admin"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/token", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token gerado com sucesso!")
        print(f"Expira em: {token_data['expires_at']}")
        print("-" * 50)
        return token_data["access_token"]
    else:
        print(f"Erro: {response.json()}")
        print("-" * 50)
        return None

def test_validate_token(token):
    """Testa a validação de token"""
    print("✅ Testando validação de token...")
    
    payload = {
        "token": token
    }
    
    response = requests.post(f"{BASE_URL}/auth/validate", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_protected_endpoint(token):
    """Testa endpoint protegido"""
    print("🔒 Testando endpoint protegido...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_invalid_api_key():
    """Testa com API key inválida"""
    print("❌ Testando com API key inválida...")
    
    payload = {
        "api_key": "api-key-invalida",
        "user_id": "test_user",
        "permissions": ["read"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/token", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_invalid_token():
    """Testa com token inválido"""
    print("❌ Testando com token inválido...")
    
    payload = {
        "token": "token-invalido-123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/validate", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API de Autenticação")
    print("=" * 50)
    
    try:
        # Teste 1: Health check
        test_health_check()
        
        # Teste 2: Gerar token
        token = test_generate_token()
        
        if token:
            # Teste 3: Validar token
            test_validate_token(token)
            
            # Teste 4: Endpoint protegido
            test_protected_endpoint(token)
        
        # Teste 5: API key inválida
        test_invalid_api_key()
        
        # Teste 6: Token inválido
        test_invalid_token()
        
        print("✅ Todos os testes concluídos!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API. Certifique-se de que ela está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()