from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from .models import TokenRequest, TokenResponse, TokenValidation, TokenValidationResponse
from .auth import create_access_token, verify_token, verify_api_key
from . import config

app = FastAPI(
    title="API de Autenticação e Autorização",
    description="Sistema simples para gerar e validar tokens JWT",
    version="1.0.0"
)

security = HTTPBearer()

@app.get("/")
async def root():
    """
    Endpoint de health check
    """
    return {"message": "API de Autenticação está funcionando!", "timestamp": datetime.utcnow()}

@app.post("/auth/token", response_model=TokenResponse)
async def generate_token(token_request: TokenRequest):
    """
    Gera um token JWT temporário
    """
    # Verifica se a API key é válida
    if not verify_api_key(token_request.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida"
        )
    
    # Dados para incluir no token
    token_data = {
        "user_id": token_request.user_id or "anonymous",
        "permissions": token_request.permissions or [],
        "type": "access_token"
    }
    
    # Define expiração
    expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.utcnow() + expires_delta
    
    # Cria o token
    access_token = create_access_token(data=token_data, expires_delta=expires_delta)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # em segundos
        expires_at=expires_at
    )

@app.post("/auth/validate", response_model=TokenValidationResponse)
async def validate_token(token_validation: TokenValidation):
    """
    Valida se um token JWT é válido
    """
    payload = verify_token(token_validation.token)
    
    if payload is None:
        return TokenValidationResponse(
            valid=False,
            message="Token inválido ou expirado"
        )
    
    # Verifica se o token não expirou
    exp_timestamp = payload.get("exp")
    if exp_timestamp and datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
        return TokenValidationResponse(
            valid=False,
            message="Token expirado"
        )
    
    return TokenValidationResponse(
        valid=True,
        user_id=payload.get("user_id"),
        permissions=payload.get("permissions", []),
        expires_at=datetime.utcfromtimestamp(exp_timestamp) if exp_timestamp else None,
        message="Token válido"
    )

@app.get("/auth/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Endpoint protegido que retorna informações do usuário atual
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verifica se o token não expirou
    exp_timestamp = payload.get("exp")
    if exp_timestamp and datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {
        "user_id": payload.get("user_id"),
        "permissions": payload.get("permissions", []),
        "token_type": payload.get("type"),
        "expires_at": datetime.utcfromtimestamp(exp_timestamp) if exp_timestamp else None
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint para monitoramento
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "auth-api",
        "version": "1.0.0"
    }