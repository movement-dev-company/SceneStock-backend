from fastapi import APIRouter, Depends
from core.database import get_db
from sqlalchemy.orm import Session
from . import models, oauth2

router_user = APIRouter()


@router_user.get('/me')
async def get_me(db: Session = Depends(get_db),
                 user_id: str = Depends(oauth2.require_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
