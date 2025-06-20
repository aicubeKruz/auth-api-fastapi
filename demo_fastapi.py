#!/usr/bin/env python3
"""
Demonstração da API FastAPI de autenticação
"""

from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.main import app
import json

# Criar cliente de teste
client = TestClient(app)

def demo_api():
    """Demonstra o uso da API"""
    print("🚀 Demonstração da API de Autenticação FastAPI")
    print("=" * 60)
    
    # Teste 1: Health check
    print("1. Health Check")
    print("-" * 30)
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Teste 2: Root endpoint
    print("2. Root Endpoint")
    print("-" * 30)
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Teste 3: Gerar token com API key válida
    print("3. Gerar Token (API key válida)")
    print("-" * 30)
    token_request = {
        "api_key": "api-key-super-secreta-123456789",
        "user_id": "demo_user_123",
        "permissions": ["read", "write", "admin"]
    }
    
    response = client.post("/auth/token", json=token_request)
    print(f"Status: {response.status_code}")
    print(f"Request: {json.dumps(token_request, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Guardar o token para testes posteriores
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Token gerado: {token[:50]}...")
    else:
        token = None
    print()
    
    # Teste 4: Gerar token com API key inválida
    print("4. Gerar Token (API key inválida)")
    print("-" * 30)
    invalid_request = {
        "api_key": "api-key-invalida",
        "user_id": "demo_user",
        "permissions": ["read"]
    }
    
    response = client.post("/auth/token", json=invalid_request)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    if token:
        # Teste 5: Validar token válido
        print("5. Validar Token (válido)")
        print("-" * 30)
        validation_request = {"token": token}
        response = client.post("/auth/validate", json=validation_request)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
        
        # Teste 6: Endpoint protegido com token válido
        print("6. Endpoint Protegido (token válido)")
        print("-" * 30)
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {headers}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()
    
    # Teste 7: Validar token inválido
    print("7. Validar Token (inválido)")
    print("-" * 30)
    invalid_validation = {"token": "token-super-invalido-123"}
    response = client.post("/auth/validate", json=invalid_validation)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Teste 8: Endpoint protegido sem token
    print("8. Endpoint Protegido (sem token)")
    print("-" * 30)
    response = client.get("/auth/me")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Teste 9: Endpoint protegido com token inválido
    print("9. Endpoint Protegido (token inválido)")
    print("-" * 30)
    headers = {"Authorization": "Bearer token-invalido-123"}
    response = client.get("/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    print("✅ Demonstração concluída!")
    print()
    print("📋 Resumo dos Endpoints:")
    print("GET  /              - Root endpoint")
    print("GET  /health        - Health check")
    print("POST /auth/token    - Gerar token JWT")
    print("POST /auth/validate - Validar token JWT")
    print("GET  /auth/me       - Endpoint protegido (info do usuário)")
    print()
    print("📖 Para ver a documentação interativa:")
    print("   Swagger UI: http://localhost:8000/docs")
    print("   ReDoc:      http://localhost:8000/redoc")

if __name__ == "__main__":
    demo_api()