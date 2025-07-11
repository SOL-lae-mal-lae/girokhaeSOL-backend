from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str 
    HOST: str 
    PORT: int 
    DEBUG: bool 

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
