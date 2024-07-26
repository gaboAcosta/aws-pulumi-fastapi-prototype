from jose import jwt

from api.domain.users import User


class AuthService:
    @staticmethod
    def create_token(user: User) -> str:
        return jwt.encode({
            'id': user.id,
            'email': user.email,
            'role': user.role.value
        }, "secret", algorithm="HS256")
