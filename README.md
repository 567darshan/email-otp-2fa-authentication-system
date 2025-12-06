
# 🔐 Email OTP 2FA Authentication System  
Secure Two-Factor Authentication using FastAPI + HTML Frontend

 

## 📌 Overview  
This project implements a **Two-Factor Authentication (2FA)** system using:

- Username + Password  
- Email-based One Time Password (OTP)

After login, a **6-digit OTP** is sent to the user's registered email.  
The login completes only after the correct OTP is verified.  
This improves security and prevents password-only attacks.

---

## 🚀 Features  

### ✅ User Registration  
- Username  
- Password  
- Email  
- Stores user details in an in-memory database (demo purpose)

### ✅ Login with OTP  
- Step 1 → Enter username + password  
- Step 2 → OTP sent to registered email  
- Step 3 → User enters OTP to verify and login

### ✅ Backend  
- FastAPI framework  
- OTP generator  
- Email sender (SMTP Gmail)  
- Secure verification flow

### ✅ Frontend  
- Simple UI  
- Separate pages for:
  - Home  
  - Register  
  - Login + OTP  

---

## 🏗️ Project Structure  

```

email-otp-2fa-authentication-system/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
└── frontend/
├── index.html
├── register.html
└── login.html

```

---

## ⚙️ Technologies Used  
**Backend:** FastAPI, Python, Uvicorn, SMTP  
**Frontend:** HTML, CSS, JavaScript  

---

## 🛠️ How to Run (Backend)

### 1️⃣ Install requirements  
```

cd backend
pip install -r requirements.txt

```

### 2️⃣ Start server  
```

python -m uvicorn main:app --reload

````

Backend runs at:  
`http://127.0.0.1:8000`

---

## 🖥️ How to Run (Frontend)

Simply open these files in your browser:

- `frontend/index.html`
- `frontend/register.html`
- `frontend/login.html`

No server needed for frontend.

---

## 📧 Email Setup  

In `backend/main.py`:

```python
EMAIL_ADDRESS = "your_email_here"
EMAIL_APP_PASSWORD = "your_app_password_here"
````

⚠️ Important

* Use your **Gmail** address
* Use a **Gmail App Password** (not your real password)
* **Never upload real credentials to GitHub**

---

## 🌱 Future Enhancements

* SMS OTP using Twilio or MSG91
* Store users in a real database
* JWT authentication
* OTP auto-expiry timer
* Resend OTP button

---

## 👨‍💻 Author

**Darshan A (567darshan)**
GitHub: [https://github.com/567darshan](https://github.com/567darshan)

---

