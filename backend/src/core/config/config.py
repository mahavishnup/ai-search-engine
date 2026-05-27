from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded dynamically from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application Server Configurations ---
    app_name: str = "AI Semantic Search Engine"
    api_version: str = "v1"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # --- Database Relational Connection ---
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/app.db",
    )

    # --- Security & Hashing (Phase 2) ---
    jwt_secret_key: str = "dev-only-secret-key-replace-in-production-environments"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- Vector Database Configurations (FAISS vs. Qdrant) ---
    vector_db_type: str = "faiss"  # Options: "faiss" | "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    faiss_index_path: str = "./storage/vector_store/faiss_index"

    # --- LLM & Embedding Providers (Phase 4 & 6) ---
    embedding_provider: str = (
        "ollama"  # Options: "ollama" | "local" | "groq" | "openrouter" | "openai"
    )
    llm_provider: str = (
        "groq"  # Options: "groq" | "openrouter" | "lm-studio" | "ollama"
    )
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_device: str = "cpu"  # Options: "cpu" | "cuda" | "mps"

    # API Access Credentials
    groq_api_key: str = ""
    openrouter_api_key: str = ""
    nvidia_api_key: str = ""

    # Local model server URLs
    ollama_base_url: str = "http://localhost:11434"
    lm_studio_base_url: str = "http://localhost:1234/v1"

    # --- Caching & Resilience (Phase 9) ---
    redis_url: str = "redis://localhost:6379/0"
    use_redis_cache: bool = False
