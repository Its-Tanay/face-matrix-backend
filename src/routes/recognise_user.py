from fastapi import APIRouter, UploadFile, Depends, File
from services.face_detection_service import FaceDetectionService
from services.feature_extraction_service import FeatureExtractionService
from services.similarity_search_service import SimilaritySearchService

router = APIRouter()

@router.post("/recognise_user")
async def recognise_user(
    image: UploadFile = File(...),
    face_detection_service: FaceDetectionService = Depends(),
    feature_extraction_service: FeatureExtractionService = Depends(),
    similarity_search_service: SimilaritySearchService = Depends(),
):
    image_content = await image.read()

    face_tensors, probability = await face_detection_service.detect_face(image_content)

    vectors = await feature_extraction_service.extract_features(face_tensors=face_tensors)

    match_result, cache_key = await similarity_search_service.find_match(vectors=vectors)

    if match_result:
        return {
            "status": "success",
            "message": "User recognised",
            "user": match_result
        }
    else:
        return {
            "status": "no_match",
            "message": "No matching user found.",
            "req_id": cache_key
        }