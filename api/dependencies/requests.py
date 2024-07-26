from starlette.requests import Request
from datetime import datetime
from fastapi import HTTPException


def parse_date_to_datetime(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d")


def date_query_param(request: Request) -> datetime | None:
    target_date = request.query_params.get('created_at_gte')
    if not target_date:
        return None
    try:
        return parse_date_to_datetime(target_date)
    except ValueError as e:
        raise HTTPException(422, str(e))
