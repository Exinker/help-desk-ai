import datetime
import logging

import uvicorn
from chainlit.utils import mount_chainlit
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

from config import (
    LOGGING_CONFIG,
    TRACER_CONFIG,
)


logging.basicConfig(
    datefmt='%Y-%m-%d %H:%M:%S',
    format='[%(asctime)s.%(msecs)03d] %(module)s::%(lineno)d %(levelname)-8s - %(message)s',
    level=LOGGING_CONFIG.logging_level.value,
)
LOGGER = logging.getLogger(__name__)


tracer_provider = register(
    endpoint=TRACER_CONFIG.endpoint,
    project_name=TRACER_CONFIG.project_name,
)
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


app = FastAPI()


@app.get('/app')
async def handle_root(request: Request):
    dt = datetime.datetime.now(datetime.UTC)

    return JSONResponse(
        dict(
            datetime=datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            **request.headers,
        ),
        status_code=200,
    )


mount_chainlit(app=app, target='src/chat/app.py', path='/')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=80, reload=True)
