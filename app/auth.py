from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, models, utils

# Declare separately
client_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/client/login")
ops_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ops/login")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(client_oauth2_scheme), db: Session = Depends(get_db)):
    payload = utils.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Use scheme dynamically
# Add this new method for ops explicitly
def get_current_ops_user(token: str = Depends(ops_oauth2_scheme), db: Session = Depends(get_db)):
    payload = utils.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


# Role check wrapper
def require_role(role: str):
    def role_checker(user: models.User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_checker

