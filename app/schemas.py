from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class FileUploadResponse(BaseModel):
    filename: str
    message: str

class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str
