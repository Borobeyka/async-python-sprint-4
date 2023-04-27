from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from core.config import config
from api import base


# ===============================================
#
# В докере все запускается, но на своем пк
# по адресу localhost:9999 приложение недоступно.
# Не понимаю как пофиксить эту проблему.
# Помогите, пожалуйста :)
#
# ===============================================


app = FastAPI(
    title=config.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(base.url_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.app_host,
        port=config.app_port,
        reload=True,
    )
