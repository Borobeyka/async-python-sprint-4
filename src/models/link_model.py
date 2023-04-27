from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, Column, String

from db.db import Base


class LinkModel(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    original_url = Column(String)
    short_url = Column(String)
    redirects = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
