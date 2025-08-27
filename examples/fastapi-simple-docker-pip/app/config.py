from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    title: str = Field(alias="APP_TITLE", default="note-go's API")
    version: str = Field(alias="APP_VERSION", default="0.1.2")
    stage: str = Field(alias="STAGE", default="local")


class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    smtp_host: str | None = Field(alias="EMAIL_SMTP_HOST", default=None)
    smtp_port: int | None = Field(alias="EMAIL_SMTP_PORT", default=None)
    smtp_user: str | None = Field(alias="EMAIL_SMTP_USER", default=None)
    smtp_password: str | None = Field(alias="EMAIL_SMTP_PASSWORD", default=None)
    from_email: str | None = Field(alias="EMAIL_FROM_EMAIL", default=None)
    to_email: str | None = Field(alias="EMAIL_TO_EMAIL", default=None)


class DatabaseSettings(BaseSettings):
    url: str = Field(alias="DATABASE_URL", default="sqlite:///./test.db")


class AuthSettings(BaseSettings):
    auth_provider_enabled: bool = Field(alias="AUTH_PROVIDER_ENABLED", default=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    email: EmailSettings = EmailSettings()
    database: DatabaseSettings = DatabaseSettings()
    auth_provider_enabled: bool = Field(alias="AUTH_PROVIDER_ENABLED", default=False)


settings = Settings()
