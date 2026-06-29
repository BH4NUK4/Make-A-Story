from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOW_ORIGINS: str = ''
    OPENAI_API_KEY: str

    @field_validator("ALLOW_ORIGINS")
    def parse_allow_origins(cls, v: str):
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
