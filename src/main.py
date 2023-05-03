from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.config import config
from api import base


app = FastAPI(
    title=config.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(base.url_router, prefix="/api")


def start_server():
    uvicorn.run(
        "main:app",
        host=config.app_host,
        port=config.app_port,
        reload=True,
    )


if __name__ == "__main__":
    start_server()
