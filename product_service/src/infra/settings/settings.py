from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):        
        
    # Url's 
    AUTH_BASE_URL: str
    
    # Broker params
    BROKER_STACK: str
    RABBITMQ_PRODUCT: dict
    
    # Database params
    PRODUCT_DB_STACK: str
    
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
  
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=[
            ".env",
            "../.env",
        ],
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings: Settings = Settings()
