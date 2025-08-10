from fastapi import APIRouter, HTTPException, Request, status, Depends
from app.schemas.schema import SignupRequest, SignupResponse, EmailVerificationRequest, EmailVerificationResponse, LoginRequest, LoginResponse
from app.core import database
from passlib.context import CryptContext
import jwt
import os
import uuid
import requests
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@example.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Replace send_verification_email with Resend implementation
def send_verification_email(email: str, token: str):
    if not RESEND_API_KEY:
        raise Exception("Resend API key not set")
    verify_url = f"{FRONTEND_URL}/verify?token={token}"
    subject = "Verify your email"
    html = f"""
    <p>Thank you for signing up!</p>
    <p>Please verify your email by clicking the link below:</p>
    <a href='{verify_url}'>{verify_url}</a>
    """
    payload = {
        "from": EMAIL_FROM,
        "to": [email],
        "subject": subject,
        "html": html
    }
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
    if response.status_code >= 400:
        raise Exception(f"Resend API error: {response.text}")

@auth_router.post("/signup", response_model=SignupResponse)
def signup(request: SignupRequest):
    user = database.get_user_by_email(request.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    hashed = hash_password(request.password)
    token = str(uuid.uuid4())
    database.create_user(request.email, hashed, token)
    try:
        send_verification_email(request.email, token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send verification email: {e}")
    return SignupResponse(message="Signup successful. Please check your email to verify your account.")

@auth_router.get("/verify", response_model=EmailVerificationResponse)
def verify_email(token: str):
    result = database.verify_user_email(token)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")
    return EmailVerificationResponse(message="Email verified successfully. You can now log in.")

@auth_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = database.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Email not verified.")
    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    access_token = create_access_token({"sub": user["email"]})
    return LoginResponse(access_token=access_token, token_type="bearer")
