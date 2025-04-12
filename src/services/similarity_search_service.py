from database.db import Database
import numpy as np
from typing import Tuple, Optional, Dict, Any
import uuid
from config import config
from exception.exceptions import ServiceUnavailable

class SimilaritySearchService:
    def __init__(self):
        self.db = Database(connection_string=config.DB_CONNECTION_STRING)
        self.similarity_threshold = 0.70

    async def find_match(self, vectors: np.ndarray) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            match = await self.db.find_similar_faces(
                vectors=vectors,
                threshold=self.similarity_threshold
            )

        except Exception as e:
            raise ServiceUnavailable(message="Database unavailable") from e
        
        if match:
            return match, None
        
        cache_key = str(uuid.uuid4())
        await self.db.cache_vectors(vectors=vectors, key=cache_key)
        return None, cache_key