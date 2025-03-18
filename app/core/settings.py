from functools import lru_cache 
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os


env_path = Path(".")/ ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):

    # App
    APP_NAME: str = os.environ.get("APP_NAME")
    DEBUG: bool = bool(os.environ.get("DEBUG"))
    
    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:3000")


    # PostgreSQL Database Config
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASS: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT"))
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")

    # URI de conexión de PostgreSQL
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{quote_plus(POSTGRES_PASS)}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    
    
    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD")
    

@lru_cache()
def get_settings() -> Settings:
    return Settings()