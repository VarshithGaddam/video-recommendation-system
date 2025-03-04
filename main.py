import sys
from pathlib import Path
from datetime import datetime
import logging

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from typing import List, Optional, Dict, Any
import uvicorn
import traceback

from app.models.recommendation import VideoRecommendation
from app.models.user import User
from app.services.recommendation_service import RecommendationService
from app.core.config import Settings

# Constants
CURRENT_USER = "VarshithGaddam"
CURRENT_TIME = datetime.strptime("2025-03-02 06:41:20", "%Y-%m-%d %H:%M:%S")
API_VERSION = "1.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Video Recommendation Engine",
    description=f"""
    A sophisticated recommendation system for personalized video content.
    
    Current User: {CURRENT_USER}
    Current Time (UTC): {CURRENT_TIME.strftime('%Y-%m-%d %H:%M:%S')}
    
    Features:
    - Personalized video recommendations
    - Mood-based content filtering
    - Multiple platform support (YouTube, Vimeo)
    - Real-time user preferences
    - Emotional support content
    """,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Video Recommendation Engine",
        version=API_VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom metadata
    openapi_schema["info"]["x-system-info"] = {
        "current_user": CURRENT_USER,
        "current_time": CURRENT_TIME.isoformat(),
        "supported_platforms": ["YouTube", "Vimeo"]
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add exception handler
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    stack_trace = traceback.format_exc()
    
    logger.error(f"Error occurred: {error_msg}")
    logger.debug(f"Stack trace: {stack_trace}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred. Please try again.",
            "timestamp": CURRENT_TIME.isoformat(),
            "path": str(request.url),
            "type": "error",
            "user": CURRENT_USER,
            "error_message": error_msg if app.debug else None
        }
    )

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation service
recommendation_service = RecommendationService()

@app.get("/", tags=["Root"])
async def root() -> Dict[str, Any]:
    """
    Root endpoint showing API information and available endpoints
    """
    return {
        "message": "Welcome to the Video Recommendation Engine API",
        "version": API_VERSION,
        "timestamp": CURRENT_TIME.isoformat(),
        "current_user": CURRENT_USER,
        "status": "running",
        "endpoints": {
            "recommendations": "/recommendations/",
            "mood_based": "/recommendations/mood/",
            "system_info": "/system/info",
            "platform_info": "/platforms",
            "user_preferences": "/user/preferences",
            "moods": "/moods",
            "health": "/health",
            "documentation": "/docs",
            "alternative_docs": "/redoc"
        }
    }

@app.get("/recommendations/", response_model=List[VideoRecommendation], tags=["Recommendations"])
async def get_recommendations(
    user_id: int,
    limit: Optional[int] = 10,
    mood: Optional[str] = None
) -> List[VideoRecommendation]:
    """
    Get personalized video recommendations for a user.
    
    Parameters:
    - user_id: The ID of the user requesting recommendations
    - limit: Maximum number of recommendations to return (default: 10, max: 50)
    - mood: Optional mood filter for recommendations
    
    Returns:
    - List of video recommendations tailored to the user
    """
    try:
        if limit < 1 or limit > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 50"
            )
            
        if user_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )
            
        recommendations = await recommendation_service.get_recommendations(
            user_id=user_id,
            limit=limit,
            mood=mood
        )
        
        return recommendations or []
        
    except Exception as e:
        logger.error(f"Error in get_recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@app.get("/recommendations/mood/", response_model=List[VideoRecommendation], tags=["Recommendations"])
async def get_mood_based_recommendations(
    mood: str,
    limit: Optional[int] = 10
) -> List[VideoRecommendation]:
    """
    Get video recommendations based on mood.
    
    Parameters:
    - mood: The mood to base recommendations on (e.g., "motivated", "sad", "focused")
    - limit: Maximum number of recommendations to return (default: 10, max: 50)
    
    Returns:
    - List of mood-based video recommendations
    """
    try:
        if limit < 1 or limit > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 50"
            )
            
        recommendations = await recommendation_service.get_mood_based_recommendations(
            mood=mood,
            limit=limit
        )
        
        return recommendations or []
        
    except Exception as e:
        logger.error(f"Error in get_mood_based_recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate mood-based recommendations: {str(e)}"
        )

@app.get("/system/info", tags=["System"])
async def get_system_info() -> Dict[str, Any]:
    """
    Get current system information including timestamp and user
    """
    return {
        "current_time": CURRENT_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        "current_time_utc": CURRENT_TIME.isoformat(),
        "current_user": CURRENT_USER,
        "api_version": API_VERSION,
        "system_status": "operational",
        "recommendation_service": "active",
        "supported_moods": [
            "motivated",
            "sad",
            "focused",
            "energetic",
            "relaxed",
            "productive"
        ],
        "supported_platforms": ["YouTube", "Vimeo"]
    }

@app.get("/platforms", tags=["System"])
async def get_platform_info() -> Dict[str, Any]:
    """
    Get information about supported video platforms
    """
    return recommendation_service.get_platform_info()

@app.get("/user/preferences", tags=["User"])
async def get_user_preferences(username: str) -> Dict[str, Any]:
    """
    Get user preferences and recommended content categories
    """
    if username != CURRENT_USER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {username}"
        )
    
    return {
        "username": CURRENT_USER,
        "last_active": CURRENT_TIME.isoformat(),
        "preferences": {
            "categories": [
                "Motivation",
                "Personal Development",
                "Success Stories",
                "Emotional Wellness"
            ],
            "duration_preference": "medium",
            "preferred_moods": [
                "motivated",
                "focused",
                "energetic"
            ]
        },
        "recommended_categories": [
            "Leadership",
            "Goal Setting",
            "Time Management",
            "Mental Health"
        ],
        "engagement_metrics": {
            "videos_watched": 42,
            "average_watch_time": 325,
            "favorite_category": "Motivation",
            "completion_rate": 0.87
        },
        "timestamp": CURRENT_TIME.isoformat()
    }

@app.get("/moods", tags=["System"])
async def get_supported_moods() -> Dict[str, Any]:
    """
    Get information about supported moods and their content types
    """
    return recommendation_service.get_supported_moods()

@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring system status
    """
    return {
        "status": "healthy",
        "timestamp": CURRENT_TIME.isoformat(),
        "user": CURRENT_USER,
        "version": API_VERSION,
        "environment": "production",
        "services": {
            "recommendation_engine": "operational",
            "video_platforms": "connected",
            "user_preferences": "available"
        }
    }

if __name__ == "__main__":
    logger.info(f"\nStarting Video Recommendation Engine...")
    logger.info(f"Current time (UTC): {CURRENT_TIME.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Current user: {CURRENT_USER}")
    logger.info(f"API version: {API_VERSION}")
    print(f"\nServer starting at http://localhost:8000")
    print(f"API documentation available at http://localhost:8000/docs")
    print(f"Alternative documentation at http://localhost:8000/redoc")
    print(f"Health check endpoint at http://localhost:8000/health\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
