# 🔐 Secure File Sharing System (FastAPI + SQLite)

A secure and role-based file sharing platform built using **FastAPI**, supporting:

- Email verification using Gmail SMTP
- JWT authentication
- Admin / Ops / Client roles
- File upload & secure downloads
- Swagger documentation
- SQLite with SQLAlchemy ORM

---

## 📁 Project Structure

secure-file-sharing/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── database.py # SQLAlchemy setup
│ ├── models.py # ORM Models
│ ├── schemas.py # Pydantic models
│ ├── utils.py # JWT, Password Hashing, Email
│ └── routers/
│ ├── client_user.py # Client routes
│ ├── ops_user.py # Ops routes
│ └── admin.py # Admin routes
│
├── uploads/ # Saved uploaded files
├── .env # Environment variables
├── .gitignore
├── README.md
└── requirements.txt

---

## ⚙️ Setup Instructions

### 1️⃣ Clone & Install Dependencies

```bash
git clone https://github.com/aman-singh73/file_sharing_system.git
cd secure-file-sharing
pip install -r requirements.txt


2️⃣ Environment Configuration
Create a .env file in the root directory with:

SECRET_KEY=supersecretkey
DATABASE_URL=sqlite:///./test.db

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password

ADMIN_TOKEN=supersecrettoken


 How to Generate Gmail App Password
Enable 2-Step Verification on your Gmail account
Go to https://myaccount.google.com/security

Navigate to https://myaccount.google.com/apppasswords

Choose:

App: Mail

Device: Other

Name it (e.g., "SecureApp")

Copy the generated 16-digit password and paste it in .env as EMAIL_PASS

🚀 Run the App
uvicorn app.main:app --reload

Home Page: http://localhost:8000
Swagger Docs: http://localhost:8000/docs

🔐 Roles & Auth Flow
Role	Description
Admin	Creates Ops users
Ops	Uploads files
Client	Downloads shared files
🔒 JWT-based Auth is used for all protected routes.

✅ Feature Checklist

✅ JWT Login for all roles
✅ Email verification before login
✅ Role-based route access
✅ File uploads (Ops only)
✅ Secure tokenized downloads (Client only)
✅ Admin route to create Ops
✅ Swagger + Postman Support

 Testing the API
🔑 Authentication Flow (Client)
POST /client/signup

Register client and receive verification email

Click on /client/verify-email?token=...

POST /client/login

Get JWT token

Use JWT in headers:


Authorization: Bearer <your_token>
📤 Upload File (Ops User)
POST /ops/login → get JWT
POST /ops/upload
Use form-data with key file
Add Bearer token in header
📥 Download File (Client)
GET /client/files → list files
GET /client/download/{file_id} → returns a secure JWT-based link
Open the returned secure-download link in browser

🛡️ Admin Endpoint
To create Ops users:

POST /admin/create-ops
Headers:
- x-admin-token: supersecrettoken (from .env)
Body:
{
  "email": "opsuser@example.com",
  "password": "strongpassword"
}
🧪 Using Postman (If Swagger authorize not working)

Hit login endpoint to get your token
Go to "Authorization" tab → Bearer Token → paste token
Test protected routes like:
/client/files
/client/download/{id}
/ops/upload

🧹 .gitignore

__pycache__/
.env
*.pyc
uploads/
*.sqlite3
*.db
venv/
🧬 Dependencies (in requirements.txt)

fastapi
uvicorn
python-multipart
sqlalchemy
passlib[bcrypt]
python-dotenv
jose
email-validator

📬 Support

If something isn't working:
Check .env variables
Make sure Gmail App Password is used
Console logs show email send failures

👨‍💻 Author
Built with ❤️ by Aman Singh
Bharatiya Antariksh Hackathon – CodeCrusaders Team