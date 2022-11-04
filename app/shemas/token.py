from pydantic import BaseModel


class TokenOutData(BaseModel):
    access_token: str
    type: str
