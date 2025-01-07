from fastapi import HTTPException

class BaseException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail={
            "status": "error",
            "error_code": status_code,
            "message": message,
        })

class BadRequest(BaseException):
    def __init__(self, message: str = "Bad Request"):
        super().__init__(status_code=400, message=message) 

class NotFound(BaseException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, message=message) 

class FaceNotDetected(BaseException):
    def __init__(self, message: str = "No face was detected"):
        super().__init__(status_code=400, message=message) 

class LowSimilarityScore(BaseException):
    def __init__(self, message: str = "Similarity score is below threshold"):
        super().__init__(status_code=400, message=message) 

class DuplicateEntry(BaseException):
    def __init__(self, message: str = "Duplicate Entry"):
        super().__init__(status_code=409, message=message) 

class InternalServer(BaseException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(status_code=500, message=message) 

class ServiceUnavailable(BaseException):
    def __init__(self, message: str = "Service unavailable"):
        super().__init__(status_code=503, message=message) 