"""Configuration validation for the Greenhouse API Proxy."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIConfig(BaseModel):
    """API configuration settings."""

    api_key: str = Field(..., description="Greenhouse API key")
    api_url: str = Field(
        default="https://harvest.greenhouse.io/v1",
        description="Greenhouse API base URL",
    )

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v):
        if not v or ":" not in v:
            raise ValueError("API key must contain a colon (format: key:password)")
        return v

    @field_validator("api_url")
    @classmethod
    def validate_api_url(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("API URL must start with http:// or https://")
        return v.rstrip("/")


class AppConfig(BaseModel):
    """Application configuration settings."""

    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError("Log level must be one of: {valid_levels}")
        return v.upper()


class StorageConfig(BaseModel):
    """Storage configuration settings."""

    data_dir: Path = Field(default=Path("data"), description="Data directory")
    batch_size: int = Field(
        default=100, ge=1, le=1000, description="Batch size for pagination"
    )

    @field_validator("data_dir")
    @classmethod
    def validate_data_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v


class Config(BaseModel):
    """Main configuration class."""

    model_config = ConfigDict(validate_assignment=True)

    api: APIConfig
    app: AppConfig
    storage: StorageConfig


def load_config_fromenv() -> Config:
    """Load configuration from environment variables."""
    import os

    return Config(
        api=APIConfig(
            api_key=os.getenv("GREENHOUSE_API_KEY", "dummy:key"),
            api_url=os.getenv("GREENHOUSE_API_URL", "https://harvest.greenhouse.io/v1"),
        ),
        app=AppConfig(
            debug=os.getenv("DEBUG", "False").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        ),
        storage=StorageConfig(
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            batch_size=int(os.getenv("BATCH_SIZE", "100")),
        ),
    )
