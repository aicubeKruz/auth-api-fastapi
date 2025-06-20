#!/usr/bin/env python3
"""
Script para testar a API de autenticação em produção (ClientCo Analytics)
"""

import requests
import json
import time
from datetime import datetime

# Configurações de produção
BASE_URL_APPENGINE = "https://analytics-clientco.appspot.com"
BASE_URL_CLOUDRUN = "https://auth-api-clientco-XXXXXXXXX-uc.a.run.app"  # Substituir após deploy
API_KEY = "analytics-clientco-api-key-2025-bramos-aicube-ca-production"

def test_production_api(base_url):
    """Testa a API em produção"""
    print(f"🔍 Testando API de Produção - ClientCo Analytics")
    print(f"URL: {base_url}")
    print("=" * 60)
    
    try:
        # Teste 1: Health check
        print("1. Health Check...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
        print()
        
        # Teste 2: Gerar token
        print("2. Gerando token de autenticação...")
        token_payload = {
            "api_key": API_KEY,
            "user_id": "clientco_user_001",
            "permissions": ["read", "write", "analytics", "admin"]
        }
        
        response = requests.post(
            f"{base_url}/auth/token", 
            json=token_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Token gerado com sucesso!")
            print(f"   Expires at: {token_data['expires_at']}")
            print(f"   Token: {token_data['access_token'][:50]}...")
            token = token_data["access_token"]
        else:
            print(f"❌ Erro ao gerar token: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        print()
        
        # Teste 3: Validar token
        print("3. Validando token...")
        validation_payload = {"token": token}
        response = requests.post(
            f"{base_url}/auth/validate",
            json=validation_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            validation = response.json()
            if validation["valid"]:
                print("✅ Token válido!")
                print(f"   User ID: {validation['user_id']}")
                print(f"   Permissions: {validation['permissions']}")
            else:
                print(f"❌ Token inválido: {validation['message']}")
                return False
        else:
            print(f"❌ Erro na validação: {response.status_code}")
            return False
        print()
        
        # Teste 4: Endpoint protegido
        print("4. Testando endpoint protegido...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{base_url}/auth/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ Endpoint protegido OK!")
            print(f"   User ID: {user_info['user_id']}")
            print(f"   Permissions: {user_info['permissions']}")
        else:
            print(f"❌ Erro no endpoint protegido: {response.status_code}")
            return False
        print()
        
        # Teste 5: Documentação
        print("5. Verificando documentação...")
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Documentação disponível!")
            print(f"   Swagger UI: {base_url}/docs")
            print(f"   ReDoc: {base_url}/redoc")
        else:
            print(f"⚠️  Documentação não acessível: {response.status_code}")
        print()
        
        print("🎉 Todos os testes passaram!")
        print()
        print("📋 Resumo da API em Produção:")
        print(f"   Base URL: {base_url}")
        print(f"   API Key: {API_KEY}")
        print(f"   Status: ✅ Funcionando")
        print(f"   Documentação: {base_url}/docs")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_integration_example():
    """Exemplo de integração em produção"""
    print("\n" + "="*60)
    print("📱 Exemplo de Integração em Produção")
    print("="*60)
    
    # Exemplo de uso da API em uma aplicação
    class ClientCoAuthAPI:
        def __init__(self, base_url):
            self.base_url = base_url
            self.api_key = API_KEY
            self.token = None
        
        def authenticate(self, user_id, permissions=None):
            """Autentica usuário e obtém token"""
            payload = {
                "api_key": self.api_key,
                "user_id": user_id,
                "permissions": permissions or ["read"]
            }
            
            try:
                response = requests.post(f"{self.base_url}/auth/token", json=payload)
                if response.status_code == 200:
                    self.token = response.json()["access_token"]
                    return True
                return False
            except:
                return False
        
        def make_authenticated_request(self, endpoint):
            """Faz requisição autenticada"""
            if not self.token:
                return None
            
            headers = {"Authorization": f"Bearer {self.token}"}
            try:
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
                return response.json() if response.status_code == 200 else None
            except:
                return None
    
    # Testar integração
    try:
        auth_api = ClientCoAuthAPI(BASE_URL_APPENGINE)
        
        print("🔐 Autenticando usuário...")
        if auth_api.authenticate("analytics_user_001", ["read", "write", "analytics"]):
            print("✅ Autenticação bem-sucedida!")
            
            print("📊 Obtendo dados do usuário...")
            user_data = auth_api.make_authenticated_request("/auth/me")
            if user_data:
                print(f"✅ Dados obtidos: {user_data['user_id']}")
                print(f"   Permissões: {user_data['permissions']}")
            else:
                print("❌ Erro ao obter dados do usuário")
        else:
            print("❌ Falha na autenticação")
            
    except Exception as e:
        print(f"❌ Erro na integração: {e}")

def main():
    """Executa todos os testes"""
    print("🚀 Teste de Produção - ClientCo Analytics Auth API")
    print("="*60)
    
    # Testar App Engine
    print("📍 Testando App Engine Deploy...")
    success_appengine = test_production_api(BASE_URL_APPENGINE)
    
    if success_appengine:
        print("\n🎯 Executando exemplo de integração...")
        test_integration_example()
    
    # Instruções para Cloud Run
    print("\n" + "="*60)
    print("📋 Para testar Cloud Run:")
    print("1. Obtenha a URL após o deploy:")
    print("   gcloud run services describe auth-api-clientco --region us-central1 --format='value(status.url)'")
    print("2. Substitua BASE_URL_CLOUDRUN no código")
    print("3. Execute: python test_production.py")
    
    print("\n🔧 Comandos úteis:")
    print("gcloud app logs tail                                    # Logs App Engine")
    print("gcloud run services logs read auth-api-clientco --region us-central1  # Logs Cloud Run")
    print("gcloud app browse                                       # Abrir App Engine")
    
    if success_appengine:
        print("\n✅ API em produção está funcionando perfeitamente!")
    else:
        print("\n❌ Verifique se o deploy foi realizado com sucesso")

if __name__ == "__main__":
    main()