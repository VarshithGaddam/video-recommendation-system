from typing import List, Optional
import time
from collections import OrderedDict

class RecommendationCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.cache = OrderedDict()
        self.timestamps = {}
    
    def get_recommendations(self, user_id: int) -> Optional[List[dict]]:
        """
        Get cached recommendations for a user if they exist and haven't expired
        """
        if user_id in self.cache:
            if self._is_valid(user_id):
                # Move to end to mark as recently used
                self.cache.move_to_end(user_id)
                return self.cache[user_id]
            else:
                # Remove expired entry
                self._remove_entry(user_id)
        return None
    
    def store_recommendations(self, user_id: int, recommendations: List[dict]):
        """
        Store recommendations in cache
        """
        # Remove oldest entry if cache is full
        if len(self.cache) >= self.max_size:
            self._remove_oldest()
        
        self.cache[user_id] = recommendations
        self.timestamps[user_id] = time.time()
        self.cache.move_to_end(user_id)
    
    def _is_valid(self, user_id: int) -> bool:
        """
        Check if cached entry is still valid
        """
        if user_id in self.timestamps:
            return (time.time() - self.timestamps[user_id]) < self.ttl
        return False
    
    def _remove_entry(self, user_id: int):
        """
        Remove an entry from cache and timestamps
        """
        self.cache.pop(user_id, None)
        self.timestamps.pop(user_id, None)
    
    def _remove_oldest(self):
        """
        Remove the oldest entry from cache
        """
        if self.cache:
            oldest = next(iter(self.cache))
            self._remove_entry(oldest)