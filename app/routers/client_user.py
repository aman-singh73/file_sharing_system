from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from .. import models, schemas, utils, auth
import os

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    # ✅ Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = utils.hash_password(user.password)
    token = utils.generate_token()
    
    new_user = models.User(
        email=user.email,
        password=hashed_pw,
        role="client",
        verification_token=token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    encrypted_url = f"http://localhost:8000/client/verify-email?token={token}"
    return {"message": "Signup successful", "verify_link": encrypted_url}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid token")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified"}

@router.post("/login", response_model=schemas.Token)
def login(user_cred: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    if not user or not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    token = utils.create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/files")
def list_files(db: Session = Depends(auth.get_db), user: models.User = Depends(auth.require_role("client"))):
    files = db.query(models.File).all()
    return [{"id": f.id, "filename": f.filename} for f in files]

@router.get("/download/{file_id}", response_model=schemas.DownloadLinkResponse)
def download(file_id: int, user: models.User = Depends(auth.require_role("client"))):
    token = utils.create_access_token({"sub": user.id, "file_id": file_id})
    return {
        "download_link": f"http://localhost:8000/client/secure-download/{token}",
        "message": "success"
    }

@router.get("/secure-download/{token}")
def secure_download(token: str, db: Session = Depends(auth.get_db)):
    payload = utils.verify_token(token)
    if not payload or "file_id" not in payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can download files")

    file = db.query(models.File).filter(models.File.id == payload.get("file_id")).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file.filepath, filename=file.filename)
