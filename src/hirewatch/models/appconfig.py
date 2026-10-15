from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Scheduling and state location"""

    model_config = SettingsConfigDict(env_prefix="HIREWATCH_", env_file=".env", extra="ignore")

    loop: bool = True
    schedule_at: str = "08:00"
    state_path: str = "state.json"
