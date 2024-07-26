"""Template App
"""
import logging
from typing import Annotated, List, Callable

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from api.domain.users.user_model import User, UserRoles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/")


def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        return User(
            id=int(decoded['id']),
            email=decoded['email'],
            role=decoded['role']
        )
    except Exception as e:
        logging.exception(e)
        raise HTTPException(401, 'Unauthorized')


def get_user_with_roles(roles: List[UserRoles]) -> Callable[[User], User]:
    def _get_users_with_roles(user: Annotated[User, Depends(get_user)]) -> User:
        if not user.role or user.role not in roles:
            raise HTTPException(403, 'Forbidden')
        return user

    return _get_users_with_roles


def enforce_service_admin(user: Annotated[User, Depends(get_user_with_roles([UserRoles.SERVICE_ADMIN.value]))]) -> User:
    return user


def enforce_workflow(user: Annotated[
    User, Depends(get_user_with_roles([UserRoles.SERVICE_ADMIN.value, UserRoles.WORKFLOW.value]))]) -> User:
    return user


def enforce_customer_client(
        user: Annotated[User, Depends(
            get_user_with_roles([UserRoles.SERVICE_ADMIN.value, UserRoles.CUSTOMER_CLIENT.value]))]) -> User:
    return user


def enforce_lab(user: Annotated[
    User, Depends(get_user_with_roles([UserRoles.SERVICE_ADMIN.value, UserRoles.LAB.value]))]) -> User:
    return user
