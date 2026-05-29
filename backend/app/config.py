from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

print("Looking for .env at:", ENV_PATH)
print("File exists:", ENV_PATH.exists())

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "openai/gpt-4o-mini"
    openai_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str = ""
    openrouter_app_name: str = "Prompt Lab"
    frontend_origin: str = "http://localhost:3000"
    api_secret_key: str = "dev-secret-key"

    model_config = SettingsConfigDict(env_file=ENV_PATH)

settings = Settings()