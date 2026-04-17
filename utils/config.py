from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PUBMED_BASE_URL: str
    REQUEST_DELAY: float
    RETMAX: int
    ARTICLES_OUTPUT_PATH: str


    DEFAULT_RETRIEVAL_METHOD: str
    RETRIEVAL_METHOD: str

    EMBEDDING_MODEL:str
    
    LLM_BASE_URL: str
    LLM_API_KEY: str

    RAG_MODEL: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()