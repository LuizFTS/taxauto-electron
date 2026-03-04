from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from config import settings

header_scheme = APIKeyHeader(name="Authorization")

def verify_token(token: str = Depends(header_scheme)):
    # Standard prefix "Bearer " is expected
    if token != f"Bearer {settings.PYTHON_BACKEND_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return token
