from pydantic import BaseModel, EmailStr, Field


# ------------------------
# REQUEST SCHEMAS
# ------------------------
class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# RESPONSE SCHEMAS
# ------------------------
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"