from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re

from .. import crud, schemas
from ..deps import get_db

router = APIRouter()


def is_valid_email(email: str) -> bool:
    # simple regex email validation
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


@router.post("/users/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # optional email validation if username looks like an email
    if "@" in user.username and not is_valid_email(user.username):
        raise HTTPException(status_code=400, detail="Invalid email address")
    existing = crud.get_user_by_username(db, username=user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    created = crud.create_user(db, user)
    return created
