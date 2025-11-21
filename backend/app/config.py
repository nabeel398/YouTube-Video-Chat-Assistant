from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str  # Only Groq needed now
    FAISS_INDEX_PATH: str = "instance/faiss_index"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()