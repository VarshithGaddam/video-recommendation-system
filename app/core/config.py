from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    model_config = {
        "case_sensitive": True
    }

    PROJECT_NAME: str = "Video Recommendation Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    CURRENT_USER: str = "VarshithGaddam"
    
    # Model Configuration
    MODEL_EMBEDDING_DIM: int = 128
    MODEL_HIDDEN_LAYERS: List[int] = [256, 128, 64]
    MODEL_DROPOUT_RATE: float = 0.3
    
    # Cache Configuration
    CACHE_MAX_SIZE: int = 1000
    CACHE_TTL: int = 3600  # 1 hour
    
    # API Configuration
    CORS_ORIGINS: List[str] = ["*"]

settings = Settings()