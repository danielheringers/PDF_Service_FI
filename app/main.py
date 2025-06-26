from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.router import router
from app.exceptions.handlers import manipulador_validacao
from starlette.middleware.gzip import GZipMiddleware


app = FastAPI()
Instrumentator().instrument(app).expose(app)
app.add_middleware(GZipMiddleware, minimum_size=500)

app.add_exception_handler(RequestValidationError, manipulador_validacao)

app.include_router(router)
