from pydantic import BaseModel

class UserInDB(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    profile_picture: str
