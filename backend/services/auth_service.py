from datetime import timedelta
from fastapi import HTTPException, status
from backend.database.repositories.user_repository import user_repository
from backend.utils.security import verify_password, get_password_hash, create_access_token
from backend.schemas.dto import UserRegisterRequest, UserLoginRequest, TokenResponse
from backend.config.settings import settings

class AuthService:
    async def register_user(self, req: UserRegisterRequest) -> dict:
        existing_email = await user_repository.get_by_email(req.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
            
        existing_username = await user_repository.get_by_username(req.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken."
            )

        hashed_pw = get_password_hash(req.password)
        user_data = {
            "email": req.email.lower(),
            "username": req.username.lower(),
            "full_name": req.full_name,
            "hashed_password": hashed_pw,
            "role": req.role or "radiologist",
            "is_active": True
        }
        
        created_user = await user_repository.create(user_data)
        
        # Return copy omitting hashed_password so stored record retains hash
        user_response = created_user.copy()
        user_response.pop("hashed_password", None)
        return user_response

    async def authenticate_user(self, req: UserLoginRequest) -> TokenResponse:
        # Check by email or username
        user = await user_repository.get_by_email(req.username_or_email)
        if not user:
            user = await user_repository.get_by_username(req.username_or_email)
            
        if not user or not verify_password(req.password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user["_id"], "role": user.get("role", "radiologist")},
            expires_delta=access_token_expires
        )
        
        user_info = {
            "id": user["_id"],
            "email": user["email"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user.get("role", "radiologist")
        }
        
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_info
        )

auth_service = AuthService()
