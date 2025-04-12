import torch
import numpy as np
import tritonclient.http as triton_client
from exception.exceptions import BadRequest, InternalServer
from config import config

class FeatureExtractionService:
    def __init__(self, 
                 triton_url: str = config.TRITON_URL, 
                 model_name: str = "facenet"):
        self.triton_client = triton_client.InferenceServerClient(url=triton_url)
        self.model_name = model_name

    async def extract_features(self, face_tensors: torch.Tensor) -> np.ndarray:
        if face_tensors is None or face_tensors.size(0) == 0:
            raise BadRequest(message="Invalid face tensors for feature extraction")
        
        try:
            if len(face_tensors.shape) == 3:
                face_tensors = face_tensors.unsqueeze(0)
            
            inputs = [triton_client.InferInput("input0", face_tensors.numpy().shape, "FP32")]
            inputs[0].set_data_from_numpy(face_tensors.numpy())
            outputs = [triton_client.InferRequestedOutput("output0")]
            response = self.triton_client.infer(self.model_name, inputs, outputs=outputs)
            embeddings = response.as_numpy("output0")

        except Exception as e: 
            raise InternalServer(message=f"Failed to extract features: {str(e)}") from e

        return embeddings[0]