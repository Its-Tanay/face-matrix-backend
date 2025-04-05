from fastapi import APIRouter, Depends
from models.user import UserReq
from services.user_management_service import UserManagementService

router = APIRouter()

@router.post("/add_user")
async def add_user(
        user: UserReq,
        user_management_service: UserManagementService = Depends()
    ):
    result = await user_management_service.add_user(user)
    return result