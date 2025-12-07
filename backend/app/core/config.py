from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "midi-api"
    default_tempo: int = 120
    default_duration: float = 1.0
    default_octave: int = 4

    class Config:
        env_file = ".env"

settings = Settings()
