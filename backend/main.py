from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time
import smtplib
import ssl
from email.message import EmailMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
#  GMAIL SETTINGS (SENDER ONLY)
# ==========================
# This Gmail is ONLY used to SEND emails (like a mail server).
# OTP will be sent TO the email that EACH USER registers with.
EMAIL_ADDRESS = "your_email_here"
EMAIL_APP_PASSWORD = "your_app_password_here"
# NOTE: Replace with real Gmail & App Password when running locally.
# Do NOT upload real credentials to GitHub.
      # <-- put 16-char app password


# ==========================
#  IN-MEMORY USER DATABASE
# ==========================
# Stores: username -> {password, email}
USERS_DB = {}

# username -> { code, expires_at }
OTP_STORE = {}
OTP_VALIDITY_SECONDS = 300  # 5 minutes


# ===========
#  MODELS
# ===========
class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class LoginStep1Request(BaseModel):
    username: str
    password: str


class OTPVerifyRequest(BaseModel):
    username: str
    otp: str


# ==========================
#  EMAIL SENDER FUNCTION
# ==========================
def send_email_otp(to_email: str, otp_code: str):
    subject = "Your OTP for 2FA Login"
    body = f"""
Hello,

Your One-Time Password (OTP) for login is: {otp_code}

This OTP is valid for {OTP_VALIDITY_SECONDS // 60} minutes.

If you did not request this, please ignore this email.

Regards,
2FA Demo System
"""

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS          # sender (your Gmail)
    msg["To"] = to_email                 # receiver (user's registered email)
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)


# ==========================
#  API ROUTES
# ==========================

@app.get("/")
def root():
    return {"message": "2FA Email OTP backend running"}


# -------- REGISTER USER --------
@app.post("/register")
def register_user(req: RegisterRequest):
    username = req.username.strip()
    password = req.password.strip()
    email = req.email.strip()

    if not username or not password or not email:
        return {"success": False, "message": "All fields are required."}

    if "@" not in email:
        return {"success": False, "message": "Invalid email address."}

    if username in USERS_DB:
        return {"success": False, "message": "Username already exists. Please choose another."}

    USERS_DB[username] = {
        "password": password,
        "email": email
    }

    return {
        "success": True,
        "message": f"User '{username}' registered successfully with email {email}."
    }


# -------- LOGIN STEP 1: CHECK PASSWORD + SEND OTP --------
@app.post("/login-step1")
def login_step1(req: LoginStep1Request):
    username = req.username.strip()
    password = req.password.strip()

    # 1. Check user exists
    if username not in USERS_DB:
        return {"success": False, "message": "Invalid username or password."}

    # 2. Check password
    if USERS_DB[username]["password"] != password:
        return {"success": False, "message": "Invalid username or password."}

    # 3. Get registered email for this user
    user_email = USERS_DB[username]["email"]

    # 4. Generate OTP
    otp_code = f"{random.randint(100000, 999999)}"
    expires_at = time.time() + OTP_VALIDITY_SECONDS

    OTP_STORE[username] = {
        "code": otp_code,
        "expires_at": expires_at
    }

    # 5. Send OTP to that user's email
    try:
        send_email_otp(user_email, otp_code)
    except Exception as e:
        return {
            "success": False,
            "message": f"Password OK, but failed to send OTP email. Error: {str(e)}"
        }

    return {
        "success": True,
        "message": f"Password verified. OTP sent to registered email: {user_email}",
        "valid_for_seconds": OTP_VALIDITY_SECONDS
    }


# -------- LOGIN STEP 2: VERIFY OTP --------
@app.post("/verify-otp")
def verify_otp(req: OTPVerifyRequest):
    username = req.username.strip()
    otp = req.otp.strip()

    if username not in OTP_STORE:
        return {"success": False, "message": "No OTP found. Please login again."}

    otp_data = OTP_STORE[username]
    now = time.time()

    if now > otp_data["expires_at"]:
        del OTP_STORE[username]
        return {"success": False, "message": "OTP expired. Please login again."}

    if otp != otp_data["code"]:
        return {"success": False, "message": "Incorrect OTP. Please try again."}

    del OTP_STORE[username]
    return {"success": True, "message": f"2FA successful. User '{username}' is fully authenticated."}
