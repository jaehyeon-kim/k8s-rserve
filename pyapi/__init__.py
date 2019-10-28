import os

os.environ["JWT_SECRET"] = "chickenAndSons"

import time
import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Body
from pydantic import BaseModel, Schema
from starlette.requests import Request

from .src.bearer import JWTBearer
from .src.bearer import encode_token

app = FastAPI(title="Rserve demo", version="0.0.1")

auth = JWTBearer()


class TokenResp(BaseModel):
    token: str


@app.get("/auth/debug/{username}", response_model=TokenResp, tags=["debug"])
async def get_token(username: str):
    return encode_token(username)


class TestResp(BaseModel):
    value: int = Schema(..., ge=0, description="value")


@app.post(
    "/rserve/test",
    summary="test function",
    response_model=TestResp,
    tags=["rserve"],
    dependencies=[Depends(auth)],
)
async def function_test(*, value: int = Body(..., ge=0, embed=True)):
    """
    Make POST request to `test` function to Rserve
    - **value** - value to be requested (and returned)
    """
    return {"value": value}
