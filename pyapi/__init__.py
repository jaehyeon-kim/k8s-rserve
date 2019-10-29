import os

os.environ["RSERVE_HOST"] = "localhost"
os.environ["RSERVE_PORT"] = "8000"
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


class ReqModel(BaseModel):
    n: float
    wait: float = None


class RespModel(BaseModel):
    n: float
    wait: float
    hostname: str


@app.post(
    "/rserve/test",
    summary="test function",
    response_model=RespModel,
    tags=["rserve"],
    dependencies=[Depends(auth)],
)
async def function_test(*, req: ReqModel):
    """
    Make POST request to `test` function to Rserve
    - **n** - value to be requested
    - **wait** - time to be delayed
    """
    url = "http://{0}:{1}/{2}".format(os.environ["RSERVE_HOST"], os.environ["RSERVE_PORT"], "test")
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=req.json())
        return r.json()
