import datetime
from pydantic import BaseModel

class UserReq(BaseModel):
    name: str
    birthdate: datetime.date
    req_id: str

class UserRes(BaseModel):
    message: str
    user_id: str