from pydantic_settings import BaseSettings, SettingsConfigDict
from src.domain.enums import Environment, ServiceCommunication 
from src.infra.schemas.broker.nats import NatsParams
import os

class Settings(BaseSettings):
    
    ENVIRONMENT: Environment
    
    AUTH_BASE_URL: str
    PRODUCT_BASE_URL: str
    ORDER_BASE_URL: str

    AUTH_COMMUNICATION_TYPE: ServiceCommunication
    PRODUCT_COMMUNICATION_TYPE: ServiceCommunication
    ORDER_COMMUNICATION_TYPE: ServiceCommunication
    
    NATS: NatsParams    
            
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
