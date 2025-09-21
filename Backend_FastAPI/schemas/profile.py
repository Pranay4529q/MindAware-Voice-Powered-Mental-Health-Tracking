from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileResponse(BaseModel):
    username: str
    email: str
    created_at: str

class UpdateProfileRequest(BaseModel):
    email: Optional[EmailStr] = None