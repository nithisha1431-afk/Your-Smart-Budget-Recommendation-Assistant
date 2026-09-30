from typing import List, Dict

from pydantic import BaseModel, Field, EmailStr, field_validator


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    room_type: str = Field(min_length=2, max_length=60)
    style: str = "Modern"
    items: List[str] = []
    quantities: Dict[str, int] = {}

    @field_validator("quantities")
    @classmethod
    def validate_quantities(cls, value):
        if any(
            quantity < 1 or quantity > 100
            for quantity in value.values()
        ):
            raise ValueError(
                "Quantities must be between 1 and 100"
            )

        return value


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    event_type: str = Field(min_length=2, max_length=60)
    guests: int = Field(gt=0, le=5000)
    venue: str = "Flexible"
    preferences: str = ""


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"