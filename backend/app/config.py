from functools import lru_cache
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = "AI-Based GitHub Repository Analyzer"
    github_api_url: str = "https://api.github.com"
    github_api_version: str = os.getenv("GITHUB_API_VERSION", "2026-03-10")
    github_token: str | None = os.getenv("GITHUB_TOKEN")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    max_files: int = int(os.getenv("MAX_FILES", "80"))
    max_file_bytes: int = int(os.getenv("MAX_FILE_BYTES", "200000"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
