from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.batch_link import BatchLink

from services.link import LinkService


url_router = APIRouter()


@url_router.post("/create", description="Создание короткой ссылки", response_model=Dict[str, str]) # noqa e501
async def create(*, batch: BatchLink, db: AsyncSession = Depends(get_session)):
    return await LinkService(db).create_links(batch)


@url_router.get("/ping", description="Проверка доступности БД", response_model=Dict[str, str])
async def ping(*, db: AsyncSession = Depends(get_session)):
    return await LinkService(db).check_connection()


@url_router.get("/{short_url}/status", description="Получение статистики URL", response_model=Dict)
async def delete_link(short_url: str, *, db: AsyncSession = Depends(get_session)) -> Dict: # noqa e501
    return await LinkService(db).get_stats(short_url)


@url_router.delete("/{short_url}", description="Удаление ссылки", response_model=Dict[str, str])
async def delete_link(short_url: str, *, db: AsyncSession = Depends(get_session)) -> Dict[str, str]: # noqa e501
    return await LinkService(db).delete_link(short_url)


@url_router.get("/{short_url}", description="Получение полной ссылки из короткой", response_model=Dict[str, str]) # noqa e501
async def get_link(short_url: str, *, db: AsyncSession = Depends(get_session)) -> Dict[str, str]: # noqa e501
    result = await LinkService(db).get_link(short_url)
    if result is None:
        raise HTTPException(status_code=410, detail="Gone")
    return result
