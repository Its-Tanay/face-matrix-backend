from services.face_detection_service import FaceDetectionService
from PIL import Image 
import io
import pytest
from facenet_pytorch import MTCNN
from unittest.mock import AsyncMock, patch, MagicMock
import torch
from exception.exceptions import FaceNotDetected

@pytest.fixture
def face_detection_service():
    return FaceDetectionService()

@pytest.fixture
def generate_mock_image():
    img = Image.new("RGB", (200, 200), color="blue")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

@pytest.fixture
def generate_large_image():
    img = Image.new("RGB", (5000, 5000), color="blue")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

def test_optimise_image_sync_resize(face_detection_service, generate_large_image):
    image = face_detection_service.optimise_image_sync(generate_large_image)
    assert max(image.size) == face_detection_service.max_image_size

def test_optimise_image_sync_rgb_conversion(face_detection_service, generate_mock_image):
    img = Image.open(io.BytesIO(generate_mock_image)).convert("L")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    converted_img = face_detection_service.optimise_image_sync(img_bytes.getvalue())
    assert converted_img.mode == "RGB"

@pytest.mark.asyncio
async def test_optimise_image(face_detection_service, generate_large_image):
    image = await face_detection_service.optimise_image(generate_large_image)
    assert max(image.size) == face_detection_service.max_image_size

@pytest.mark.asyncio
@patch.object(MTCNN, '__call__', new_callable=MagicMock)
async def test_detect_face_success(mock_mtcnn, face_detection_service, generate_mock_image):
    print(f"{mock_mtcnn} ffffffffffffffffffffffffffffff")
    mock_mtcnn.return_value = (torch.rand(1, 2, 160, 160), 0.99)
    face_tensor, prob = await face_detection_service.detect_face(generate_mock_image)
    assert face_tensor is not None
    assert prob >= face_detection_service.threshold

@pytest.mark.asyncio
@patch.object(MTCNN, '__call__', new_callable=MagicMock)
async def test_detect_face_no_face(mock_mtcnn, face_detection_service, generate_mock_image):
    mock_mtcnn.return_value = (None, 0)
    with pytest.raises(FaceNotDetected):
        await face_detection_service.detect_face(generate_mock_image)