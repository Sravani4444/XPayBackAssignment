from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: str  # This will store the path or identifier of the profile picture
