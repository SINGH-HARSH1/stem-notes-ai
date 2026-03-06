from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, RedisDsn, SecretStr, model_validator, Field


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AppConfig(BaseModel):
    name: str = Field(default="STEM Notes AI")
    version: str = Field(default="0.1.0")
    debug: bool = False
    env: Literal["local", "dev", "staging", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @model_validator(mode="after")
    def validate_prod(self):
        if self.env == "prod" and self.debug:
            raise ValueError("SECURITY RISK: Debug cannot be enabled in production environment.")
        return self

class ApiConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=2, ge=1, le=16)

class DatabaseConfig(BaseModel):
    url: PostgresDsn

class BrokerConfig(BaseModel):
    url: RedisDsn

class AiProviderConfig(BaseModel):
    openai_api_key: SecretStr
    llm_model_name: str = "gpt-4o"

class Settings(BaseSettings):
    app: AppConfig = Field(default_factory=AppConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    ai: AiProviderConfig = Field(default_factory=AiProviderConfig)


    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env" if (BASE_DIR / ".env").exists() else None,
        env_nested_delimiter='__',
        case_sensitive=False,
        extra="ignore",
        validate_default=True
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Dependency Injection provider for settings.
    Using lru_cache ensures we don't re-read settings multiple times.
    """
    return Settings()

settings = get_settings()

