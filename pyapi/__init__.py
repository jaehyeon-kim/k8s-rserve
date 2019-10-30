import os
import time
import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Body
from pydantic import BaseModel, Schema
from starlette.requests import Request

from .src.bearer import JWTBearer
from .src.bearer import encode_token

app = FastAPI(title="Rserve sidecar demo", version="0.0.1")

auth = JWTBearer()


class TokenResp(BaseModel):
    token: str


@app.get("/auth/debug/{username}", response_model=TokenResp, tags=["debug"])
async def get_token(username: str):
    return encode_token(username)


class ReqModel(BaseModel):
    n: float
    wait: float = Schema(None, gt=0, le=1)


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
    - **wait** - time to be delayed, greater than 1 and less than or equal to 1
    """
    host = os.getenv("RSERVE_HOST", "localhost")
    port = os.getenv("RSERVE_PORT", "8000")
    async with httpx.AsyncClient() as client:
        r = await client.post("http://{0}:{1}/{2}".format(host, port, "test"), json=req.json())
        return r.json()
