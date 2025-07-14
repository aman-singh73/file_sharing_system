from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.utils import hash_password, generate_token
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


@router.post("/admin/create-ops")
def create_ops_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role="ops",
        is_verified=True,
        verification_token=generate_token()
    )
    db.add(new_user)
    db.commit()
    return {"message": f"Ops user '{user.email}' created successfully"}
