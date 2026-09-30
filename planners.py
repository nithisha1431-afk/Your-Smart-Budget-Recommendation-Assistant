from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from app.config import settings
from app.dependencies import current_user
from app.models.schemas import (
    HomeRequest,
    PartyRequest,
)
from app.services.gemini import generate
from app.services.store import (
    save_recommendation,
)


router = APIRouter()


def save_result(
    planner,
    data,
    result,
    user,
):
    save_recommendation(
        user["id"],
        planner,
        float(data["budget"]),
        data,
        result,
    )

    return result


@router.post("/generate-home")
def generate_home(
    data: HomeRequest,
    user=Depends(current_user),
):
    request_data = data.model_dump()

    result = generate(
        "home",
        request_data,
    )

    return save_result(
        "home",
        request_data,
        result,
        user,
    )


@router.post("/generate-party")
def generate_party(
    data: PartyRequest,
    user=Depends(current_user),
):
    request_data = data.model_dump()

    result = generate(
        "party",
        request_data,
    )

    return save_result(
        "party",
        request_data,
        result,
        user,
    )


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Elegant"),
    outfit_color: str = Form(""),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(
        default=None
    ),
    user=Depends(current_user),
):

    if budget <= 0:
        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero",
        )

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_color": outfit_color,
        "notes": notes,
    }

    image_bytes = None
    mime_type = "image/jpeg"

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):
            raise HTTPException(
                status_code=415,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are supported"
                ),
            )

        image_bytes = await (
            outfit_image.read()
        )

        max_size = (
            settings.max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=413,
                detail="Image is too large",
            )

        mime_type = (
            outfit_image.content_type
        )

    result = generate(
        "jewelry",
        data,
        image_bytes,
        mime_type,
    )

    return save_result(
        "jewelry",
        data,
        result,
        user,
    )