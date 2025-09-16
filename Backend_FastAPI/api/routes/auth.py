from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from services.auth_service import AuthService
from models.user import User
from schemas.auth import RegisterRequest, LoginRequest, LoginResponse

router = APIRouter()

@router.post("/register")
async def register_user(
    user_data: RegisterRequest,
    auth_service: AuthService = Depends(lambda: AuthService())
):
    """Register a new user"""
    
    # Create user
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    return JSONResponse(
        content={"message": "User registered successfully"},
        status_code=status.HTTP_201_CREATED
    )

@router.post("/login", response_model=LoginResponse)
async def login_user(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(lambda: AuthService())
):
    """Login a user"""
    
    # Verify user credentials
    user = await User.verify_password(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate token
    access_token = auth_service.generate_token({"username": login_data.username})
    
    return LoginResponse(
        message="Login successful",
        access_token=access_token,
        username=login_data.username,
        token_type="bearer"
    )