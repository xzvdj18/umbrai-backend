from datetime import datetime
from pydantic import BaseModel, EmailStr

# --- مخططات رسائل الاتصال (Contact Form) ---
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- مخططات المستخدمين (Users) ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- مخططات الـ Tokens ---
class Token(BaseModel):
    access_token: str
    token_type: str