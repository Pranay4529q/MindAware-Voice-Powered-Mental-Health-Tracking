from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from dependencies import get_current_user
from models.user import User
from schemas.profile import ProfileResponse, UpdateProfileRequest

router = APIRouter()

@router.get("/profile", response_model=ProfileResponse)
async def get_user_profile(
    current_user: str = Depends(get_current_user)
):
    """Get the current user's profile"""
    
    user = await User.get_by_username(current_user)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return ProfileResponse(
        username=user['username'],
        email=user['email'],
        created_at=user['created_at'].isoformat()
    )

@router.put("/profile")
async def update_user_profile(
    profile_data: UpdateProfileRequest,
    current_user: str = Depends(get_current_user)
):
    """Update the current user's profile"""
    
    # Update user
    updated_user = await User.update_profile(
        username=current_user,
        update_data=profile_data.dict(exclude_unset=True)
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or no changes made"
        )
    
    return JSONResponse(
        content={
            "message": "Profile updated successfully",
            "username": updated_user['username'],
            "email": updated_user['email']
        },
        status_code=200
    )