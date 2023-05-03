import pytest
from httpx import AsyncClient

from core.config import config
from main import app


@pytest.mark.asyncio
async def test():
    async def test_ping():
        async with AsyncClient(app=app, base_url=f"http://{config.app_prefix}") as client:
            response = await client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

    async def test_url_status():
        short_url = "88b954e01a07"
        async with AsyncClient(app=app, base_url=f"http://{config.app_prefix}") as client:
            response = await client.get(f"/{short_url}/status")
        assert response.status_code == 200
        assert response.json() == {
            "id": 6,
            "original_url": "vk.com",
            "short_url": "88b954e01a07",
            "redirects": 4,
            "created_at": "2023-04-26T17:25:12.659065",
            "is_deleted": False
        }

    async def test_get_link():
        short_link = "0a9803b3a043"
        async with AsyncClient(app=app, base_url=f"http://{config.app_prefix}") as client:
            response = await client.get(f"/{short_link}")
        assert response.status_code == 200
        assert response.json() == {
            "original_url": "yandex.ru"
        }

    await test_ping()
    await test_url_status()
    await test_get_link()
