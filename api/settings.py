import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ENV: str = os.environ.get('ENV', 'local')
    USE_SOCKET_CONNECTION: bool = os.environ.get('USE_SOCKET_CONNECTION', 'False')
    ENCRYPT_SECRET: str = os.environ.get("ENCRYPT_SECRET", "")
    DATABASE_HOST: str = os.environ["DATABASE_HOST"]
    DATABASE_USER: str = os.environ["DATABASE_USER"]
    DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    DATABASE_PORT: int = os.environ.get("DATABASE_PORT", 5432)
    ORDRS_DOMAIN: str = os.environ.get('ORDRS_DOMAIN', 'https://demo-api.ordrs.io')
    ORDRS_API_KEY: str = os.environ.get("ORDRS_API_KEY", "Kk4FGx-sXhA63-.w98Zk")
    ORDRS_CLIENT_ID: str = os.environ.get("ORDRS_CLIENT_ID",
                                          "2179447e446af545464377a9b367e7eac8874590899611e8e8694cf1bf852d4e")
    ORDRS_SECRET: str = os.environ.get("ORDRS_SECRET", "dzB./5xupX3g/aUNTsdMztJoh12t1osH2Y.")

    CREATE_REQUISITION_WORKFLOW: str = os.environ.get("CREATE_ORDER_WORKFLOW", "requisitions-dev-create-requisition")
    UPDATE_REQUISITION_STATUS_WORKFLOW: str = os.environ.get(
        "UPDATE_REQUISITION_STATUS_WORKFLOW", "requisitions-dev-update-requisition-status")
    CREATE_REQUISITION_RESULTS_WORKFLOW: str = os.environ.get(
        "CREATE_REQUISITION_RESULTS_WORKFLOW", "requisitions-dev-create-requisition-results")
    SENTRY_DSN: str = os.environ.get('SENTRY_DSN', '')


settings = Settings()
