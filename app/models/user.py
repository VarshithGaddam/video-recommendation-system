from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "VarshithGaddam",
                "preferences": {
                    "categories": ["Motivation", "Personal Development"],
                    "duration_preference": "medium"
                },
                "watch_history": [1, 2, 3],
                "mood_preferences": ["motivated", "focused"],
                "created_at": "2025-03-02T06:18:45",
                "last_active": "2025-03-02T06:18:45"
            }
        }
    )

    id: int
    username: str
    preferences: Optional[dict] = {}
    watch_history: List[int] = []
    mood_preferences: List[str] = []
    created_at: datetime
    last_active: datetime