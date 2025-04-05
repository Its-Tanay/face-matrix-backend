import pytest
from unittest.mock import patch, MagicMock
import torch
import numpy as np
from services.feature_extraction_service import FeatureExtractionService
from facenet_pytorch import InceptionResnetV1
from exception.exceptions import BadRequest

@pytest.fixture
def feature_extraction_service():
    return FeatureExtractionService()

@pytest.fixture
def generate_mock_face_tensors():
    return torch.rand(1, 3, 160, 160)

@pytest.mark.asyncio
@patch.object(InceptionResnetV1, 'forward', new_callable=MagicMock)
async def test_feature_extraction_success(mock_model, generate_mock_face_tensors, feature_extraction_service):
    mock_model.return_value = torch.rand(1, 512)
    features = await feature_extraction_service.extract_features(generate_mock_face_tensors)
    assert isinstance(features, np.ndarray)
    assert features.shape == (512,)

@pytest.mark.asyncio
async def test_feature_extraction_invalid_tensors(feature_extraction_service):
    with pytest.raises(BadRequest) as exc_info:
        await feature_extraction_service.extract_features(None)
    assert exc_info.value.detail["message"] == "Invalid face tensors for feature extraction"