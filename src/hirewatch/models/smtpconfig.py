from pydantic_settings import BaseSettings, SettingsConfigDict


class SmtpConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")

    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_pass: str
    mail_from: str
    mail_to: str
