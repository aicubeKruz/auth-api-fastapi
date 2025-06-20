#!/usr/bin/env python3
"""
Exemplo de cliente para a API de Autenticação
Demonstra como integrar com a API em uma aplicação real
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

class AuthClient:
    """Cliente para a API de Autenticação"""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Inicializa o cliente
        
        Args:
            base_url: URL base da API (ex: https://sua-api.com)
            api_key: Chave da API para gerar tokens
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.current_token = None
        self.token_expires_at = None
    
    def generate_token(self, user_id: str, permissions: list = None) -> Dict[str, Any]:
        """
        Gera um novo token JWT
        
        Args:
            user_id: ID do usuário
            permissions: Lista de permissões
            
        Returns:
            Dados do token gerado
        """
        url = f"{self.base_url}/auth/token"
        payload = {
            "api_key": self.api_key,
            "user_id": user_id,
            "permissions": permissions or []
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        token_data = response.json()
        
        # Armazenar token para uso posterior
        self.current_token = token_data["access_token"]
        self.token_expires_at = datetime.fromisoformat(
            token_data["expires_at"].replace('Z', '+00:00')
        )
        
        return token_data
    
    def validate_token(self, token: str = None) -> Dict[str, Any]:
        """
        Valida um token JWT
        
        Args:
            token: Token a ser validado (usa o token atual se não especificado)
            
        Returns:
            Resultado da validação
        """
        url = f"{self.base_url}/auth/validate"
        token_to_validate = token or self.current_token
        
        if not token_to_validate:
            raise ValueError("Nenhum token disponível para validação")
        
        payload = {"token": token_to_validate}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_current_user(self, token: str = None) -> Dict[str, Any]:
        """
        Obtém informações do usuário atual
        
        Args:
            token: Token de autorização (usa o token atual se não especificado)
            
        Returns:
            Informações do usuário
        """
        url = f"{self.base_url}/auth/me"
        token_to_use = token or self.current_token
        
        if not token_to_use:
            raise ValueError("Nenhum token disponível para autorização")
        
        headers = {"Authorization": f"Bearer {token_to_use}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def is_token_valid(self) -> bool:
        """
        Verifica se o token atual ainda é válido
        
        Returns:
            True se o token é válido, False caso contrário
        """
        if not self.current_token:
            return False
        
        try:
            validation = self.validate_token()
            return validation.get("valid", False)
        except:
            return False
    
    def ensure_valid_token(self, user_id: str, permissions: list = None):
        """
        Garante que há um token válido, gerando um novo se necessário
        
        Args:
            user_id: ID do usuário (para gerar novo token se necessário)
            permissions: Permissões (para gerar novo token se necessário)
        """
        if not self.is_token_valid():
            print("🔄 Token inválido ou expirado, gerando novo token...")
            self.generate_token(user_id, permissions)
            print("✅ Novo token gerado")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica se a API está funcionando
        
        Returns:
            Status da API
        """
        url = f"{self.base_url}/health"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

def demo_client():
    """Demonstra o uso do cliente"""
    print("🚀 Demonstração do Cliente de Autenticação")
    print("=" * 50)
    
    # Configurar cliente
    client = AuthClient(
        base_url="http://localhost:8000",
        api_key="api-key-super-secreta-123456789"
    )
    
    try:
        # 1. Health check
        print("1. Verificando status da API...")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Serviço: {health['service']} v{health['version']}")
        print()
        
        # 2. Gerar token
        print("2. Gerando token...")
        user_id = "cliente_demo_123"
        permissions = ["read", "write", "admin"]
        
        token_data = client.generate_token(user_id, permissions)
        print(f"   Token gerado para usuário: {user_id}")
        print(f"   Expira em: {token_data['expires_at']}")
        print(f"   Token: {token_data['access_token'][:50]}...")
        print()
        
        # 3. Validar token
        print("3. Validando token...")
        validation = client.validate_token()
        print(f"   Válido: {validation['valid']}")
        print(f"   Usuário: {validation['user_id']}")
        print(f"   Permissões: {validation['permissions']}")
        print()
        
        # 4. Obter informações do usuário
        print("4. Obtendo informações do usuário...")
        user_info = client.get_current_user()
        print(f"   ID: {user_info['user_id']}")
        print(f"   Permissões: {user_info['permissions']}")
        print(f"   Tipo do token: {user_info['token_type']}")
        print()
        
        # 5. Demonstrar renovação automática
        print("5. Demonstrando verificação automática de token...")
        print(f"   Token atual válido: {client.is_token_valid()}")
        
        # Garantir token válido (não fará nada se já for válido)
        client.ensure_valid_token(user_id, permissions)
        print(f"   Token após verificação: {client.is_token_valid()}")
        print()
        
        # 6. Exemplo de uso em aplicação
        print("6. Exemplo de uso em aplicação...")
        print("   # Fazer requisições autenticadas:")
        print(f"   headers = {{'Authorization': 'Bearer {client.current_token[:30]}...'}}")
        print("   response = requests.get('https://sua-api.com/dados', headers=headers)")
        print()
        
        print("✅ Demonstração concluída com sucesso!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        print("   Execute: ./scripts/run_dev.sh")
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        print(f"   Response: {e.response.text}")
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

class ExampleApplication:
    """Exemplo de como integrar o cliente em uma aplicação"""
    
    def __init__(self):
        self.auth_client = AuthClient(
            base_url="http://localhost:8000",
            api_key="api-key-super-secreta-123456789"
        )
        self.user_id = "app_user_456"
        self.permissions = ["read", "write"]
    
    def protected_operation(self):
        """Exemplo de operação que requer autenticação"""
        # Garantir que temos um token válido
        self.auth_client.ensure_valid_token(self.user_id, self.permissions)
        
        # Fazer requisição autenticada
        try:
            user_info = self.auth_client.get_current_user()
            print(f"Operação autorizada para usuário: {user_info['user_id']}")
            return True
        except Exception as e:
            print(f"Erro na operação protegida: {e}")
            return False
    
    def run(self):
        """Executa a aplicação exemplo"""
        print("\n🏢 Exemplo de Aplicação com Autenticação")
        print("-" * 40)
        
        success = self.protected_operation()
        if success:
            print("✅ Aplicação executada com sucesso!")
        else:
            print("❌ Falha na execução da aplicação")

if __name__ == "__main__":
    # Executar demonstração do cliente
    demo_client()
    
    # Executar exemplo de aplicação
    try:
        app = ExampleApplication()
        app.run()
    except Exception as e:
        print(f"\n❌ Erro na aplicação exemplo: {e}")