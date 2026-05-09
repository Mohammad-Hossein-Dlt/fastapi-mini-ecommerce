from src.domain.enums import Environment
from src.infra.schemas.broker.rabbitmq import RabbitParams
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    
    ENVIRONMENT: Environment
    RABBITMQ: RabbitParams
    AUTH_BASE_URL: str
    PRODUCT_BASE_URL: str
    ORDER_BASE_URL: str
            
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=[
            f".env.{os.getenv("ENVIRONMENT", "dev")}",
            f"../.env.{os.getenv("ENVIRONMENT", "dev")}",
        ],
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings: Settings = Settings()
