from pydantic import BaseModel


class NetworkRequest(BaseModel):
    total: int
    js: int
    css: int
