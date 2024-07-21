from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str
    phone: str

class UserCreate(UserBase):
    full_name: str
    profile_picture: str  # This will store the path or identifier of the profile picture in MongoDB

class UserInDB(UserBase):
    id: int
    full_name: str
