
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_users():
    return {"users": []}
