from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from backend.app.core.security import hash_password
from backend.app.database import engine, Base, get_db
from backend.app.models.users_model import User
from backend.app.config import BASE_DIR
from backend.app.routes import login, users, backup

load_dotenv()

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
            role="admin",
            is_active=True
        ))
        db.commit()

    return {"success": True}
