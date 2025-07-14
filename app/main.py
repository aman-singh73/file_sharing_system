from fastapi import FastAPI
from .database import Base, engine
from .routers import ops_user, client_user
from app.routers import client_user, ops_user, admin
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse

load_dotenv() 
Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Secure File Sharing</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(120deg, #2c3e50, #3498db);
                    color: white;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    text-align: center;
                }
                h1 {
                    font-size: 3rem;
                    margin-bottom: 0.5rem;
                }
                p {
                    font-size: 1.2rem;
                    margin-bottom: 2rem;
                }
                a {
                    padding: 12px 24px;
                    background-color: #ffffff;
                    color: #2c3e50;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    transition: background-color 0.3s ease;
                }
                a:hover {
                    background-color: #f0f0f0;
                }
                .logo {
                    font-size: 4rem;
                    margin-bottom: 1rem;
                    animation: popIn 1s ease;
                }
                @keyframes popIn {
                    0% { transform: scale(0.5); opacity: 0; }
                    100% { transform: scale(1); opacity: 1; }
                }
            </style>
        </head>
        <body>
            <div class="logo">🔐</div>
            <h1>Secure File Sharing System</h1>
            <p>Welcome to your backend service powered by FastAPI.</p>
            <a href="/docs">Go to API Documentation</a>
        </body>
    </html>
    """

app.include_router(ops_user.router)
app.include_router(client_user.router)
app.include_router(admin.router)