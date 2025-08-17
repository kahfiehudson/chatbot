import os

class Settings:
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name: str = os.getenv("MODEL_NAME", "mistral:7b")
    system_prompt: str = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")

settings = Settings()
