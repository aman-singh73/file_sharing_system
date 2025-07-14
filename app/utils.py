from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
import uuid
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
EMAIL_USER = os.getenv("EMAIL_USER")
print(EMAIL_USER)
EMAIL_PASS = os.getenv("EMAIL_PASS")
print(EMAIL_PASS)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])  # ensure string for JWT
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Valid token payload:", payload)
        return payload
    except JWTError as e:
        print("JWT decode error:", e)
        return None

def generate_token() -> str:
    return str(uuid.uuid4())

def send_verification_email(to_email: str, token: str):
    verify_url = f"http://localhost:8000/client/verify-email?token={token}"
    subject = "Verify Your Email - Secure File Sharing"
    body = f"""
    <h2>Welcome!</h2>
    <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
    <a href="{verify_url}">{verify_url}</a>
    <p>This link will expire soon for your security.</p>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print("✅ Verification email sent.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
