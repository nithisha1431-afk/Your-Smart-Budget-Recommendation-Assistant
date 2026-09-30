from fastapi import (
    APIRouter,
    HTTPException,
    Response,
)

from app.config import settings
from app.models.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.services.store import (
    create_user,
    get_user_by_email,
)


router = APIRouter()


@router.post("/register")
def register(data: RegisterRequest):

    if get_user_by_email(data.email):
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user_id = create_user(
        data.name.strip(),
        data.email,
        hash_password(data.password),
    )

    return {
        "message": "Registration successful",
        "user_id": user_id,
    }


@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
):

    user = get_user_by_email(
        data.email
    )

    if (
        not user
        or not verify_password(
            data.password,
            user["password_hash"],
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        user["id"],
        user["email"],
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=7200,
    )

    return {
        "message": "Login successful"
    }


@router.post(
    "/token",
    response_model=TokenResponse
)
def token(data: LoginRequest):

    user = get_user_by_email(
        data.email
    )

    if (
        not user
        or not verify_password(
            data.password,
            user["password_hash"],
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(
            user["id"],
            user["email"],
        ),
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out"
    }