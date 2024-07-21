from pydantic import BaseModel

class UserInDB(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    profile_picture_path: str  # Assuming this is the path to profile picture stored in MongoDB
