from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.core.security import hash_password
from app.database import engine, Base, get_db
from app.models.users_model import User
from app.config import BASE_DIR
from app.routes import login, home, users, backup

load_dotenv()

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI()

app.mount("/static",StaticFiles(directory=BASE_DIR / "static"), name="static")

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(home.router)
app.include_router(users.router)
app.include_router(backup.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        db.add(User(
            first_name="admin",
            last_name="admin",
            username="admin",
            password=hash_password("123"),
            role="admin"
        ))

    return templates.TemplateResponse("login.html", {"request": request})