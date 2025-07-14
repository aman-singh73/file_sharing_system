from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, auth
import os
import shutil
from fastapi import Security

router = APIRouter(prefix="/ops", tags=["Ops"])

@router.post("/login", response_model=schemas.Token)
def login(user_cred: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    if not user or not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Only ops users can login here")
    token = utils.create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/upload", response_model=schemas.FileUploadResponse)
def upload_file(file: UploadFile = File(...),  current_user: models.User = Depends(auth.get_current_ops_user),  db: Session = Depends(auth.get_db)):
    allowed_extensions = ["pptx", "docx", "xlsx"]
    ext = file.filename.split(".")[-1]
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.File(filename=file.filename, filepath=path, uploaded_by=current_user.id)
    db.add(new_file)
    db.commit()

    return {"filename": file.filename, "message": "Upload successful"}
