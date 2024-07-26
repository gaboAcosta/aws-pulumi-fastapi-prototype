from api.common.base_service import BaseService
from . import User, UserCreationRequestSchema, UserUpdateSchema


class UsersService(BaseService):
    def list_users(self):
        return self.db.query(User).all()

    def create_user(self, user_data: UserCreationRequestSchema) -> User:
        user = User(
            email=user_data.email,
            role=user_data.role,
        )
        user.set_password(user_data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_data: UserUpdateSchema):
        user = self.find_or_fail(User, id=user_id)
        if user_data.role:
            user.role = user_data.role
        if user_data.password:
            user.set_password(user_data.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email) -> User:
        return self.find_or_fail(User, email=email)

    def get_or_create_user_in_db(self, uid: str, email: str) -> User:
        user = self.db.query(User).filter_by(external_id=uid).first()
        if not user:
            user = User(email=email, role='CLIENT')
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user

    def get_user_with_credentials(self, email: str, password: str):
        user = self.get_user_by_email(email)
        user.check_password(password)
        return user
