# 🚀 Como Usar o Sistema de Autenticação

## 📋 Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação e Configuração

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Edite o arquivo `.env` com suas chaves:
```env
SECRET_KEY=sua-chave-secreta-super-forte-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_KEY=sua-api-key-super-secreta
```

### 3. Iniciar a aplicação
```bash
# Modo desenvolvimento
./scripts/run_dev.sh

# OU manualmente
uvicorn app.main:app --reload
```

## 🧪 Testando a API

### Testes Básicos
```bash
# Testar funções localmente (sem servidor)
python test_local.py

# Demonstração completa da API
python demo_fastapi.py

# Exemplo de cliente Python
python client_example.py
```

### Testes com Servidor Rodando
```bash
# Iniciar servidor em um terminal
./scripts/run_dev.sh

# Em outro terminal, executar testes
./scripts/test_api.sh
```

## 📖 Acessar Documentação

Com o servidor rodando, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Fluxo de Autenticação

### 1. Gerar Token
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sua-api-key-super-secreta",
    "user_id": "usuario123",
    "permissions": ["read", "write"]
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "expires_at": "2025-06-20T12:00:00"
}
```

### 2. Validar Token
```bash
curl -X POST http://localhost:8000/auth/validate \
  -H "Content-Type: application/json" \
  -d '{
    "token": "SEU_TOKEN_AQUI"
  }'
```

**Resposta:**
```json
{
  "valid": true,
  "user_id": "usuario123",
  "permissions": ["read", "write"],
  "expires_at": "2025-06-20T12:00:00",
  "message": "Token válido"
}
```

### 3. Usar Token em Endpoints Protegidos
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "user_id": "usuario123",
  "permissions": ["read", "write"],
  "token_type": "access_token",
  "expires_at": "2025-06-20T12:00:00"
}
```

## 🐳 Usando Docker

### Desenvolvimento
```bash
docker-compose up --build
```

### Produção
```bash
# Build da imagem
docker build -t auth-api .

# Executar container
docker run -p 8000:8000 -e SECRET_KEY=sua-chave auth-api
```

## ☁️ Deploy no Google Cloud

### App Engine
```bash
# Configurar projeto
gcloud config set project SEU-PROJECT-ID

# Deploy
gcloud app deploy app.yaml

# OU usar script
./scripts/deploy_gcp.sh
```

### Cloud Run
```bash
# Deploy com Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

## 🔐 Segurança

### Chaves Importantes
1. **SECRET_KEY**: Chave para assinar tokens JWT
2. **API_KEY**: Chave para controlar quem pode gerar tokens

### Boas Práticas
- Use chaves fortes e únicas
- Configure HTTPS em produção
- Monitore logs de autenticação
- Implemente rate limiting
- Use tempo de expiração apropriado

## 🛠️ Integração com Sua Aplicação

### Python
```python
from client_example import AuthClient

# Inicializar cliente
auth = AuthClient("https://sua-api.com", "sua-api-key")

# Gerar token
token = auth.generate_token("user123", ["read", "write"])

# Fazer requisições autenticadas
response = auth.get_current_user()
```

### JavaScript
```javascript
// Gerar token
const response = await fetch('https://sua-api.com/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        api_key: 'sua-api-key',
        user_id: 'user123',
        permissions: ['read', 'write']
    })
});

const { access_token } = await response.json();

// Usar token
const userData = await fetch('https://sua-api.com/auth/me', {
    headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## 🐛 Solução de Problemas

### Erro: "API key inválida"
- Verifique se a API_KEY no .env está correta
- Confirme que está usando a mesma chave na requisição

### Erro: "Token inválido ou expirado"
- Gere um novo token
- Verifique se o token não expirou
- Confirme que o SECRET_KEY não mudou

### Erro: "Connection refused"
- Certifique-se que o servidor está rodando
- Verifique se a porta 8000 está disponível
- Confirme a URL da API

### Erro: "Not authenticated"
- Inclua o header Authorization: Bearer <token>
- Verifique se o token é válido

## 📊 Monitoramento

### Logs
```bash
# Ver logs do container
docker-compose logs -f

# Logs do App Engine
gcloud app logs tail
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🔧 Personalização

### Alterar Tempo de Expiração
No arquivo `.env`:
```env
ACCESS_TOKEN_EXPIRE_MINUTES=60  # 1 hora
```

### Adicionar Novos Endpoints
1. Edite `app/main.py`
2. Adicione novos endpoints
3. Use `Depends(security)` para proteger endpoints

### Modificar Estrutura do Token
1. Edite `app/auth.py`
2. Modifique a função `create_access_token`
3. Atualize validações conforme necessário

## 📞 Suporte

Para problemas ou dúvidas:
1. Consulte os logs da aplicação
2. Verifique a documentação em `/docs`
3. Execute os testes para diagnosticar problemas
4. Verifique as configurações de ambiente

---

✅ **Pronto! Sua API de autenticação está funcionando!**