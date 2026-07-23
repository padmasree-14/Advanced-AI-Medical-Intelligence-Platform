from fastapi import APIRouter, Depends, status
from backend.schemas.dto import UserRegisterRequest, UserLoginRequest, TokenResponse, StandardResponse
from backend.services.auth_service import auth_service
from backend.services.audit_service import audit_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def register(req: UserRegisterRequest):
    user = await auth_service.register_user(req)
    await audit_service.log_action("USER_REGISTER", "users", user_id=user["_id"])
    return StandardResponse(
        success=True,
        message="User registered successfully.",
        data=user
    )

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest):
    token_resp = await auth_service.authenticate_user(req)
    await audit_service.log_action("USER_LOGIN", "auth", user_id=token_resp.user["id"])
    return token_resp
