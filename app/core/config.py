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

    # JWT 설정
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24

    CLERK_SECRET_KEY: str
    CLERK_KEY_URL: str

    KIWOOM_APP_KEY: str
    KIWOOM_SECRET_KEY: str
    KIWOOM_BASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()