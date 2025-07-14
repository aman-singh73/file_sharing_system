import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Secure File Sharing"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_TOKEN_EXPIRE_MINUTES: int = 15
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    EMAIL_USER: str = os.getenv("EMAIL_USER", "youremail@example.com")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS", "yourpassword")

settings = Settings()
