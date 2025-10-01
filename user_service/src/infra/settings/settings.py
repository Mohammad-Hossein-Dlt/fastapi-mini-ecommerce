from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # EXTERNAL_FASTAPI_PORT: int
    # INTERNAL_FASTAPI_PORT: int
    
    # AUTH_BASE_URL: str
    # PRODUCT_BASE_URL: str
    # ORDER_BASE_URL: str
            
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings: Settings = Settings()
