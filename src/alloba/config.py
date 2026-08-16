from pathlib import Path

from pydantic_settings import BaseSettings

_REPO_ROOT = Path(__file__).resolve().parents[2]

_DEFAULT_ORIGINS = "http://localhost:3005,http://localhost:8582"


class Settings(BaseSettings):
    # Platform backend (ispaces Commerce / AfroMART) this gateway proxies to.
    backend_url: str = "http://localhost:8561"
    # FAISS knowledge engine.
    rag_index_dir: str = str(_REPO_ROOT / "rag_index")
    rag_docs_dir: str = str(_REPO_ROOT / "kb" / "docs")
    embedding_model: str = "nomic-embed-text"
    rag_top_k: int = 4
    # Local LLM (Ollama).
    ollama_base_url: str = "http://127.0.0.1:11434"
    llm_model: str = "llama3.2:1b"
    # HTTP surface.
    allowed_origins: str = _DEFAULT_ORIGINS
    host: str = "0.0.0.0"
    port: int = 8582
    # Agentic sourcing.
    agent_mode: str = "auto"
    agent_tool_models: str = "qwen3.5,qwen3.6,qwen2.5,llama3.3"
    agent_max_steps: int = 6
    agent_default_language: str = "en"

    model_config = {"env_prefix": "ALLOBA_"}


settings = Settings()
