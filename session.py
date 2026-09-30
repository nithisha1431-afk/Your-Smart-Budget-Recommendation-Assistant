from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies import current_user
from app.services.store import history


router = APIRouter()


@router.get("/session-info")
def session_info(
    user=Depends(current_user)
):
    return {
        "logged_in": True,
        "user_id": user["id"],
        "email": user["email"],
    }


@router.get("/session-data")
def session_data(
    user=Depends(current_user)
):
    return {
        "user": user,
        "recent": history(
            user["id"],
            5
        ),
    }


@router.get("/history")
def recommendation_history(
    user=Depends(current_user)
):
    return {
        "history": history(
            user["id"]
        )
    }