from __future__ import annotations
from typing import List
from pydantic import BaseModel

from models.link import Link


class BatchLink(BaseModel):
    urls: List[Link]
