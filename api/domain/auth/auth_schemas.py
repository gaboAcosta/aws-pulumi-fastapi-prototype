from pydantic import BaseModel


class AuthenticationSchema(BaseModel):
    access_token: str
