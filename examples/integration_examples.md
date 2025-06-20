# 🔗 Exemplos de Integração

Esta API pode ser integrada com qualquer linguagem que suporte HTTP. Aqui estão exemplos práticos:

## 🐍 Python

### Usando requests
```python
import requests

class AuthAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.token = None
    
    def get_token(self, user_id, permissions=None):
        response = requests.post(f"{self.base_url}/auth/token", json={
            "api_key": self.api_key,
            "user_id": user_id,
            "permissions": permissions or []
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return self.token
        return None
    
    def make_authenticated_request(self, url):
        headers = {"Authorization": f"Bearer {self.token}"}
        return requests.get(url, headers=headers)

# Uso
auth = AuthAPI("https://sua-api.com", "sua-api-key")
token = auth.get_token("user123", ["read", "write"])
response = auth.make_authenticated_request("https://sua-api.com/dados")
```

## 🟨 JavaScript/Node.js

### Usando fetch
```javascript
class AuthAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.token = null;
    }
    
    async getToken(userId, permissions = []) {
        const response = await fetch(`${this.baseUrl}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                api_key: this.apiKey,
                user_id: userId,
                permissions: permissions
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.token = data.access_token;
            return this.token;
        }
        return null;
    }
}

// Uso
const auth = new AuthAPI('https://sua-api.com', 'sua-api-key');
const token = await auth.getToken('user123', ['read', 'write']);
```

## 🌐 cURL (Terminal)

### Gerar token
```bash
curl -X POST https://sua-api.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sua-api-key",
    "user_id": "user123",
    "permissions": ["read", "write"]
  }'
```

### Usar token
```bash
# Salvar token
TOKEN=$(curl -s -X POST https://sua-api.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "sua-api-key", "user_id": "user123"}' \
  | jq -r '.access_token')

# Requisição autenticada
curl -X GET https://sua-api.com/dados \
  -H "Authorization: Bearer $TOKEN"
```

## ☕ Java

```java
import java.net.http.*;
import java.net.URI;

public class AuthAPI {
    private final String baseUrl;
    private final String apiKey;
    private String token;
    private final HttpClient client;
    
    public AuthAPI(String baseUrl, String apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.client = HttpClient.newHttpClient();
    }
    
    public String getToken(String userId) throws Exception {
        String requestBody = String.format(
            "{\"api_key\":\"%s\",\"user_id\":\"%s\"}", 
            apiKey, userId
        );
        
        var request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/auth/token"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();
        
        var response = client.send(request, HttpResponse.BodyHandlers.ofString());
        
        if (response.statusCode() == 200) {
            // Parse JSON response para extrair token
            // Implementar parser JSON aqui
            return "token_extraido";
        }
        return null;
    }
}
```

---

💡 **Dica**: Sempre implemente cache para tokens válidos e trate erros de rede adequadamente!