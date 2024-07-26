from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.domain.auth import AuthenticationSchema, AuthService
from api.domain.users import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login/", response_model=AuthenticationSchema)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    users_service = UsersService(db)
    database_user = users_service.get_user_with_credentials(
        email=form_data.username,
        password=form_data.password
    )
    access_token = AuthService.create_token(database_user)
    return {"access_token": access_token, "token_type": "bearer"}
