from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()

async def get_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme"
        )

    return credentials.credentials