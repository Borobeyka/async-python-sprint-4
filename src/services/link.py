import uuid
from fastapi import HTTPException
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.batch_link import BatchLink
from models.reponse_models import (
    ResponseCreatedLinks,
    ResponseDBConnection,
    ResponseDeleteLink,
    ResponseLinkStats,
    ResponseLinkURL
)

from services.logger import logger
from core.config import config
from models.link_model import LinkModel
from models.short_link import ShortLink


class LinkService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self, short_url: str) -> ResponseLinkStats:
        logger_prefix = f"Request statistics for \"{config.app_prefix}{short_url}\""
        statement = (
            select(LinkModel)
            .where(LinkModel.short_url == short_url) # noqa E712
        )
        obj = (await self.session.execute(statement=statement)).scalar_one_or_none()
        if obj is None or obj.is_deleted:
            logger.debug(f"{logger_prefix}, status: 404 Not found")
            raise HTTPException(status_code=404)
        logger.debug(f"{logger_prefix}, status: OK")
        return ResponseLinkStats(**obj.__dict__)

    async def delete_link(self, short_url: str) -> ResponseDeleteLink:
        logger_prefix = f"Delete link \"{config.app_prefix}{short_url}\""
        statement = (
            update(LinkModel)
            .where(LinkModel.short_url == short_url) # noqa E712
            .values(is_deleted=True)
        )
        await self.session.execute(statement=statement)
        await self.session.commit()
        logger.debug(f"{logger_prefix}, status: OK")
        return ResponseDeleteLink(
            status="OK"
        )

    async def get_link(self, short_url: str) -> ResponseLinkURL:
        logger_prefix = f"Request original link for \"{config.app_prefix}{short_url}\""
        statement = (
            select(LinkModel)
            .where(
                and_(
                    LinkModel.short_url == short_url,
                    LinkModel.is_deleted == False # noqa E712
                )
            )
        )
        await self.session.commit()
        obj = (await self.session.execute(statement=statement)).scalar_one_or_none()
        if obj is None:
            logger.debug(f"{logger_prefix}, status: 410 Gone")
            return None
        obj.redirects += 1
        await self.session.commit()
        logger.debug(f"{logger_prefix}, status: OK")
        return ResponseLinkURL(
            original_url=obj.original_url
        )

    async def create_links(self, batch: BatchLink):
        result = []
        for link in batch.urls:
            link = LinkModel(
                original_url=link.url,
                short_url=str(uuid.uuid4()).split("-")[-1]
            )
            self.session.add(link)
            await self.session.commit()
            logger.debug(f"Create short link for \"{link.original_url}\", status: OK")
            result.append(ShortLink(url=f"{config.app_prefix}{link.short_url}"))
        return ResponseCreatedLinks(
            status="OK",
            links=[{"url": short_link.url} for short_link in result]
        )

    async def check_connection(self) -> ResponseDBConnection:
        res = await self.session.execute(statement=select(LinkModel))
        status = "OK" if res else "DOWN"
        logger.debug(f"Check connection to DB, status: {status}")
        return ResponseDBConnection(
            status=status
        )
