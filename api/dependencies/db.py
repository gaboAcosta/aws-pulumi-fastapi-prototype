import logging

from ..database import SessionLocal, get_db_url
from ..settings import settings

# Dependency
def get_db():
    url = get_db_url()
    print(f"settings: {settings}!")
    print(f"Database URL: {url.render_as_string(hide_password=False)}")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
