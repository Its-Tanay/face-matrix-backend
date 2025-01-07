import torch
from facenet_pytorch import MTCNN
from PIL import Image
from typing import Tuple, Optional
import io
import asyncio
from exception.exceptions import FaceNotDetected, LowSimilarityScore, InternalServer

class FaceDetectionService:
    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.detector = MTCNN(
            image_size=160,
            margin=0,
            min_face_size=20,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            device=self.device
        )
        self.threshold = 0.95
        self.max_image_size = 1024

    def optimise_image_sync(self, image_bytes: bytes) -> Image.Image:
        image = Image.open(io.BytesIO(image_bytes))

        if max(image.size) > self.max_image_size:
            ratio = self.max_image_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.LANCZOS)

        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image

    async def optimise_image(self, image: bytes) -> Image.Image:
        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(None, self.optimise_image_sync, image)
        return image
        
    async def detect_face(self, image_bytes: bytes) -> Optional[Tuple[torch.Tensor, float]]:
        image = await self.optimise_image(image=image_bytes)

        try:
            face_tensor, prob = self.detector(image, return_prob=True)

        except Exception as e:
            raise InternalServer(f"Something went wrong, try again later")
        
        if face_tensor is None:
            raise FaceNotDetected
        
        if prob < self.threshold:
            raise LowSimilarityScore
        
        return face_tensor, prob