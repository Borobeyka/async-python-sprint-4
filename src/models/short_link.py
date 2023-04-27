from pydantic import BaseModel


class ShortLink(BaseModel):
    url: str
