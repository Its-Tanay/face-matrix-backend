from database.db import Database
from models.user import UserReq, UserRes
import uuid
import config
from exception.exceptions import InternalServer

class UserManagementService:
    def __init__(self):
        self.db = Database(connection_string=config.DB_CONNECTION_STRING)

    async def add_user(self, req: UserReq) -> UserRes:

        vectors = await self.db.get_cached_vectors(key=req.req_id)
        
        try:
            user_id = str(uuid.uuid4())

            await self.db.add_user(
                user_id=user_id,
                name=req.name,
                birthdate=req.birthdate,
                face_vectors=vectors
            )
            
            await self.db.delete_cached_vectors(key=req.req_id)
            
            return UserRes(
                message=f"{req.name} was added",
                user_id=user_id
            )
        
        except Exception as e:
            raise InternalServer(message="Failed to add user") from e