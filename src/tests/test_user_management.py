import pytest
from services.user_management_service import UserManagementService
from unittest.mock import AsyncMock
from models.user import UserReq, UserRes
import numpy as np

@pytest.fixture
def user_management_service():
    service = UserManagementService()
    service.db = AsyncMock()
    service.cache = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_add_user_success(user_management_service):
    req = UserReq(
        name="Tanay",
        birthdate="2002-02-20",
        req_id="12345"
    )
    mock_vectors = np.random.rand(512)
    mock_res = {
        "id": "12345678",
        "name": "Tanay",
        "birthdate": "2002-02-20"
    }
    user_management_service.cache.get_cached_vectors.return_value = mock_vectors
    user_management_service.db.add_user.return_value = mock_res
    user_management_service.cache.delete_cached_vectors.return_value = None
    result = await user_management_service.add_user(req)
    assert isinstance(result, UserRes)
    assert result.message == "Tanay was added"
    assert isinstance(result.user_id, str)
    assert len(result.user_id) > 0