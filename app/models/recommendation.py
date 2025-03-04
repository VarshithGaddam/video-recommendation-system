from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class VideoRecommendation(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Motivational Morning Routine",
                "description": "Start your day with this energizing routine",
                "url": "https://example.com/video1",
                "thumbnail_url": "https://example.com/thumb1.jpg",
                "duration": 300,
                "category": "Motivation",
                "tags": ["morning", "routine", "motivation"],
                "mood_tags": ["energetic", "positive"],
                "engagement_score": 0.95,
                "created_at": "2025-03-02T06:18:45"
            }
        }
    )

    id: int
    title: str
    description: Optional[str] = None
    url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None  # duration in seconds
    category: Optional[str] = None
    tags: List[str] = []
    mood_tags: List[str] = []
    engagement_score: float
    created_at: datetime
