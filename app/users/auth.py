from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, oauth2, schemas
from core.config import settings
from core.database import get_db
from core.hashing import verify_password

router_token = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60


@router_token.post('/login',)
async def login(request: schemas.LoginUser,
                response: Response,
                db: Session = Depends(get_db),
                Authorize: oauth2.AuthJWT = Depends()):
    user = db.query(models.User).filter(
        models.User.email == request.email).first()
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
    response.set_cookie(key='access_token',
                        value=access_token,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
                        httponly=True)
    response.set_cookie(key='refresh_token',
                        value=refresh_token,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
                        httponly=True)
    response.set_cookie(key='logged_in',
                        value='True',
                        max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
                        httponly=True)
    return user


@router_token.get('/refresh')
async def refresh_token(response: Response,
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

    response.set_cookie(key='access_token',
                        value=access_token,
                        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
                        httponly=True)
    response.set_cookie(key='logged_in',
                        value='True',
                        max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
                        httponly=True)
    return {'access_token': access_token}


@router_token.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response,
                 Authorize: oauth2.AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
