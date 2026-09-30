import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "PocketSmart AI")
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-change-me"
    )
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash"
    )
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pocketsmart.db"
    )
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000"
    )
    max_upload_mb: int = int(
        os.getenv("MAX_UPLOAD_MB", "5")
    )
    cookie_secure: bool = (
        os.getenv("COOKIE_SECURE", "false").lower() == "true"
    )


settings = Settings()