from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict # <-- Added SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOW_ORIGINS: str = ''
    GEMINI_API_KEY: str

    @field_validator("ALLOW_ORIGINS")
    @classmethod
    def parse_allow_origins(cls, v: str):
        return v.split(",") if v else []
    
    # --- THIS IS THE NEW V2 WAY TO LOAD .ENV FILES ---
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )