from datetime import timedelta
from fastapi import (APIRouter, Depends,
                     HTTPException, status,
                     Response, Request)
from sqlalchemy.orm import Session
from pydantic import EmailStr

from . import models, schemas, oauth2
from core.database import get_db
from core.hashing import verify_password
from core.config import settings

router_token = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


@router_token.post('/login',)
def login(request: schemas.LoginUser,
          response: Response,
          db: Session = Depends(get_db),
          Authorize: oauth2.AuthJWT = Depends()):
    user = db.query(models.User).filter(
        models.User.email == EmailStr(request.email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Некорректный email')
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Некорректный пароль')
    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    response.set_cookie('access_token', access_token,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRE_MINUTES * 60,
                        REFRESH_TOKEN_EXPIRE_MINUTES * 60,
                        '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True',
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        '/', None, False, True, 'lax')
    return {'status': 'success', 'access_token': access_token}


@router_token.get('/refresh')
def refresh_token(response: Response,
                  request: Request,
                  Authorize: oauth2.AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Не удалось обновить access token')
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Пользователь не существует')
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Пожалуйста, предоставьте refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True',
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router_token.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response,
           Authorize: oauth2.AuthJWT = Depends(),
           user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
