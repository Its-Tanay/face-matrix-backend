import pytest
from services.similarity_search_service import SimilaritySearchService
from unittest.mock import MagicMock, AsyncMock
import numpy as np

@pytest.fixture
def similarity_search_service():
    service = SimilaritySearchService()
    service.db = AsyncMock()
    service.cache = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_find_match_success(similarity_search_service):
    mock_vectors = np.random.rand(512)
    mock_result = {
        "id": "12345",
        "name": "tanay"
    }
    similarity_search_service.db.find_similar_faces.return_value = mock_result
    match, cache_key = await similarity_search_service.find_match(mock_vectors)
    assert match == mock_result
    assert cache_key is None

@pytest.mark.asyncio
async def test_find_match_no_match(similarity_search_service):
    mock_vectors = np.random.rand(512)
    similarity_search_service.db.find_similar_faces.return_value = None
    similarity_search_service.db.cache_vectors.return_value = None
    match, returned_cache_key = await similarity_search_service.find_match(mock_vectors)
    assert match is None
    assert isinstance(returned_cache_key, str)