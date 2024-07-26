import logging

from fastapi import FastAPI, APIRouter

# adding _ to make it always the first import and avoid other modules loading first
from ._setup_ import settings
from .router import base_router

description = """
Sample FastAPI Service. 🚀
"""

app = FastAPI(
    title=f"Sample Service API - {settings.ENV}",
    summary="Sample Service API",
    description=description
)

main_router = APIRouter(
    responses={404: {"description": "Not found"}},
)

@main_router.get("/")
async def ping():
    return "OK"

app.include_router(main_router)
app.include_router(base_router)

# default_app = firebase_admin.initialize_app()
