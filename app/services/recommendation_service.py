from typing import List, Optional
from datetime import datetime
import random

class RecommendationService:
    def __init__(self):
        self.current_time = datetime.strptime("2025-03-02 06:59:00", "%Y-%m-%d %H:%M:%S")
        self.current_user = "VarshithGaddam"
        
        # Base mood categories for unknown moods
        self.base_moods = {
            "positive": ["happy", "excited", "energetic", "motivated", "inspired", "cheerful", "joyful", "optimistic"],
            "negative": ["sad", "angry", "frustrated", "anxious", "depressed", "stressed", "upset", "worried"],
            "neutral": ["calm", "focused", "relaxed", "peaceful", "balanced", "mindful", "composed", "centered"],
            "emotional": ["love", "romantic", "heartbroken", "nostalgic", "sentimental", "passionate", "emotional"],
            "mental": ["confused", "thoughtful", "curious", "creative", "reflective", "intellectual", "philosophical"]
        }
        
        # Video platforms with extensive mood content
        self.video_platforms = {
            "youtube": {
                "video_url": "https://www.youtube.com/watch?v={video_id}",
                "thumbnail_url": "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                "embed_url": "https://www.youtube.com/embed/{video_id}",
                # Map of mood categories to video IDs
                "mood_videos": {
                    "positive": [
                        "ZbZSe6N_BXs",     # Happy - Pharrell Williams
                        "pRpeEdMmmQ0",     # Uptown Funk
                        "ru0K8uYEZWw",     # Can't Stop the Feeling
                        "09R8_2nJtjg",     # Shake it Off
                        "y6Sxv-sUYtM"      # Happy Day
                    ],
                    "negative": [
                        "kXYiU_JCYtU",     # Numb - Linkin Park
                        "eVTXPUF4Oz4",     # In The End
                        "04854XqcfCY",     # Human - Rag'n'Bone Man
                        "CdXesX6mYUE",     # Sound of Silence
                        "gH476CxJxfg"      # Mad World
                    ],
                    "neutral": [
                        "5qap5aO4i9A",     # lofi hip hop
                        "DWcJFNfaw9c",     # Deep Focus
                        "lTRiuFIWV54",     # Study Music
                        "1vx8iUvfyCY",     # Mind Clearing
                        "goyZbut_KFY"      # Clear Mind
                    ],
                    "emotional": [
                        "JGwWNGJdvx8",     # Perfect - Ed Sheeran
                        "0E4Crx1PXJQ",     # All of Me
                        "450p7goxZqg",     # I Will Always Love You
                        "Y8HOfcYWZoo",     # Can't Help Falling in Love
                        "rtOvBOTyX00"      # The Way You Look Tonight
                    ],
                    "mental": [
                        "DVg2EJvvlF8",     # Meditation for Clarity
                        "6kVlZAc6v3g",     # Mental Focus
                        "v7xUxQsLPDw",     # Clear Thinking
                        "1ZYbU82GVz4",     # Productive Music
                        "goGNJ6hzUHk"      # Brain Power
                    ]
                }
            }
        }

    def _categorize_mood(self, mood: str) -> str:
        """
        Categorize any given mood into one of the base categories
        """
        mood = mood.lower()
        
        # Direct match in base moods
        for category, moods in self.base_moods.items():
            if mood in moods:
                return category
                
        # Word association mapping
        mood_mappings = {
            "positive": ["good", "great", "awesome", "amazing", "wonderful", "fantastic", "excellent"],
            "negative": ["bad", "terrible", "horrible", "awful", "miserable", "down", "low"],
            "neutral": ["okay", "fine", "normal", "regular", "standard", "moderate"],
            "emotional": ["feeling", "heart", "soul", "spirit", "touched", "moved"],
            "mental": ["think", "thought", "mind", "brain", "idea", "wonder"]
        }
        
        for category, keywords in mood_mappings.items():
            if any(keyword in mood for keyword in keywords):
                return category
                
        # Default to neutral if no match found
        return "neutral"

    async def get_mood_based_recommendations(
        self,
        mood: str,
        limit: int = 10
    ) -> List[dict]:
        """
        Get recommendations for any mood
        """
        try:
            mood_category = self._categorize_mood(mood)
            platform = self.video_platforms["youtube"]
            recommendations = []
            
            # Content templates based on mood category
            templates = {
                "positive": {
                    "titles": [
                        "Feel Good Vibes: {mood}",
                        "Uplifting Moments: {mood}",
                        "Happy Times: {mood}",
                        "Positive Energy: {mood}"
                    ],
                    "descriptions": [
                        "Boost your mood with amazing content for {mood} feelings.",
                        "Perfect playlist for when you're feeling {mood}.",
                        "Keep the good vibes going with {mood} content.",
                        "Enhance your {mood} energy with these picks."
                    ]
                },
                "negative": {
                    "titles": [
                        "Finding Peace: {mood}",
                        "Healing Moments: {mood}",
                        "Understanding: {mood}",
                        "Path to Calm: {mood}"
                    ],
                    "descriptions": [
                        "Transform your {mood} energy into something positive.",
                        "Find understanding and peace when feeling {mood}.",
                        "Let the music help you process {mood} feelings.",
                        "Journey from {mood} to calm with these selections."
                    ]
                },
                "neutral": {
                    "titles": [
                        "Balance & Harmony: {mood}",
                        "Peaceful Moments: {mood}",
                        "Mindful State: {mood}",
                        "Centered Energy: {mood}"
                    ],
                    "descriptions": [
                        "Maintain your {mood} state with balanced content.",
                        "Perfect for a {mood} mindset and focused energy.",
                        "Stay centered and {mood} with these picks.",
                        "Enhance your {mood} state with mindful content."
                    ]
                },
                "emotional": {
                    "titles": [
                        "Heart & Soul: {mood}",
                        "Emotional Journey: {mood}",
                        "Feel Deep: {mood}",
                        "Soul Touch: {mood}"
                    ],
                    "descriptions": [
                        "Connect with your {mood} feelings through music.",
                        "Express your {mood} emotions with these selections.",
                        "Perfect for deep {mood} moments.",
                        "Let the music match your {mood} heart."
                    ]
                },
                "mental": {
                    "titles": [
                        "Mind Space: {mood}",
                        "Mental Clarity: {mood}",
                        "Think Clear: {mood}",
                        "Brain Waves: {mood}"
                    ],
                    "descriptions": [
                        "Clear your mind while feeling {mood}.",
                        "Perfect for {mood} thinking and focus.",
                        "Enhance your {mood} mental state.",
                        "Optimize your {mood} thought process."
                    ]
                }
            }
            
            template = templates[mood_category]
            
            for i in range(limit):
                video_id = random.choice(platform["mood_videos"][mood_category])
                
                video = {
                    "id": i + 1,
                    "title": random.choice(template["titles"]).format(mood=mood),
                    "description": random.choice(template["descriptions"]).format(mood=mood),
                    "url": platform["video_url"].format(video_id=video_id),
                    "thumbnail_url": platform["thumbnail_url"].format(video_id=video_id),
                    "embed_url": platform["embed_url"].format(video_id=video_id),
                    "duration": random.randint(180, 600),  # 3-10 minutes
                    "category": mood_category.capitalize(),
                    "platform": "youtube",
                    "tags": [
                        mood.lower(),
                        mood_category,
                        "recommended",
                        f"{mood}_content"
                    ],
                    "mood_tags": [mood.lower(), mood_category],
                    "engagement_score": round(0.95 - (i * 0.02), 2),
                    "created_at": self.current_time.isoformat(),
                    "metadata": {
                        "recommended_by": self.current_user,
                        "recommendation_time": self.current_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "mood_type": mood,
                        "mood_category": mood_category,
                        "content_type": f"{mood}_content",
                        "platform": "youtube",
                        "quality": "HD"
                    }
                }
                
                recommendations.append(video)
            
            return recommendations
            
        except Exception as e:
            print(f"Error in get_mood_based_recommendations: {str(e)}")
            raise Exception(f"Failed to generate mood-based recommendations: {str(e)}")

    def get_supported_moods(self) -> dict:
        """
        Get information about all supported moods
        """
        all_moods = []
        for category, moods in self.base_moods.items():
            all_moods.extend(moods)
            
        return {
            "timestamp": self.current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.current_user,
            "supported_mood_categories": list(self.base_moods.keys()),
            "all_supported_moods": sorted(all_moods),
            "mood_categories": self.base_moods,
            "total_moods": len(all_moods)
        }