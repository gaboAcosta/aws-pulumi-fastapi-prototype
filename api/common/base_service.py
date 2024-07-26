from fastapi import HTTPException
from api.domain.users import User


class BaseService:
    def __init__(self, db, user: User | None = None):
        self.db = db
        if user:
            self.has_all_user_access = user.has_all_user_access

    def not_found_error(self, error_response: str):
        raise HTTPException(404, error_response)

    def bad_request_error(self, error_response: str):
        raise HTTPException(400, error_response)

    def find_or_fail(self, model, **kwargs):
        instance = self.db.query(model).filter_by(**kwargs).first()
        if not instance:
            return self.not_found_error("Not Found")
        return instance

    def fail_or_return(self, result, message):
        if not result:
            return self.not_found_error(message)
        return result

    def create_instance(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def save_instance(self, instance):
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def filter_for_user(self, query):
        if self.has_all_user_access:
            return query
        return query.filter_by(organization_id=self.organization_id)
