import os
from typing import Dict, Optional, List

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED


def encode_token(username: str):
    claims = {"sub": username, "debug": True}
    token = jwt.encode(claims, os.getenv("JWT_SECRET", "chickenAndSons"), algorithm="HS256")
    return {"token": token}


def decode_token(token: str):
    claims = jwt.decode(token, os.getenv("JWT_SECRET", "chickenAndSons"), algorithms=["HS256"])
    return claims


class JWTAuthorizationInfo(BaseModel):
    jwt_token: str
    claims: Dict[str, str]


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(scheme_name="Simple JWT Bearer", auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[JWTAuthorizationInfo]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        try:
            token = credentials.credentials
            auth_info = JWTAuthorizationInfo(jwt_token=token, claims=decode_token(token))
        except JWTError:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid Token")

        return auth_info
