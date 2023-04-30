from datetime import datetime
from typing import List
from pydantic import BaseModel

from models.link import Link


class ResponseCreatedLinks(BaseModel):
    status: str
    links: List[Link]


class ResponseDBConnection(BaseModel):
    status: str


class ResponseDeleteLink(BaseModel):
    status: str


class ResponseLinkURL(BaseModel):
    original_url: str


class ResponseLinkStats(BaseModel):
    id: int
    original_url: str
    short_url: str
    redirects: int
    created_at: datetime
    is_deleted: bool
