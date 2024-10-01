from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_INSIGHTS_API_KEY: str

    class Config:
        env_file = ".env"


SETTINGS = Settings()
