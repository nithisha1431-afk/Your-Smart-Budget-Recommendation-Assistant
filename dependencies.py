from fastapi import (
    Header,
    HTTPException,
    Request,
)

from app.security import decode_token


def current_user(
    request: Request,
    authorization: str | None = Header(
        default=None
    ),
):
    token = request.cookies.get(
        "access_token"
    )

    if (
        not token
        and authorization
        and authorization.lower().startswith(
            "bearer "
        )
    ):
        token = authorization.split(
            " ",
            1
        )[1]

    payload = (
        decode_token(token)
        if token
        else None
    )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Login required or token expired",
        )

    return {
        "id": int(payload["sub"]),
        "email": payload["email"],
    }