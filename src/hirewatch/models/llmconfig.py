from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class LlmConfig(BaseSettings):
    """OpenAI-compatible LLM API config."""

    model_config = SettingsConfigDict(env_prefix="LLM_", env_file=".env", extra="ignore")

    url: HttpUrl
    model: str
    prompt_override: str | None = None
    api_key: str = ""
