from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users_model import User
from app.models.permissions_model import Permission
from app.core.auth import validate_user
from app.config import BASE_DIR

router = APIRouter(prefix="/home")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# this endpoint returns the homepage for the logged in user, and his role and permissions
@router.get("/")
def get_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user_id, user_role = validate_user(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    permission_types = [p.type for p in db.query(Permission).filter(Permission.user_id == user_id).all()]

    return templates.TemplateResponse("home.html", {"request": request, "permisisons": permission_types, "role": user_role})
