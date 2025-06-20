from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenRequest(BaseModel):
    api_key: str
    user_id: Optional[str] = None
    permissions: Optional[list] = []

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    expires_at: datetime

class TokenValidation(BaseModel):
    token: str

class TokenValidationResponse(BaseModel):
    valid: bool
    user_id: Optional[str] = None
    permissions: Optional[list] = []
    expires_at: Optional[datetime] = None
    message: Optional[str] = None