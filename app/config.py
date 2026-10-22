"""Application configuration and environment variables."""
import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "generated_docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = BASE_DIR / "app" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    app_name: str = "DocAgent"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # LLM Settings
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    default_provider: str = os.getenv("DEFAULT_LLM_PROVIDER", "auto")
    
    # Storage
    docs_dir: Path = DOCS_DIR
    static_dir: Path = STATIC_DIR

settings = Settings()
