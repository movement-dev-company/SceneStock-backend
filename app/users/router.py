from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from core.database import get_db
from core.hashing import hash_password
from core.confirmation_code import create_confirmation_code
from core.send_email import send_email
from core.db_utils import check_if_already_registered


router_auth = APIRouter()


@router_auth.post(
    '/signup/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
async def signup(
    request: schemas.BaseUser, db: Session = Depends(get_db),
    code: str = Depends(create_confirmation_code),
):
    check_if_already_registered(models.User, 'email', request.email, db)
    check_if_already_registered(models.User, 'username', request.username, db)

    confirmation_code = db.query(models.ConfirmationCode).filter(
        models.ConfirmationCode.email == request.email
    ).first()

    if confirmation_code:
        confirmation_code.confirmation_code = code
    else:
        confirmation_code = models.ConfirmationCode(
            email=request.email,
            confirmation_code=code,
        )
        db.add(confirmation_code)
    db.commit()
    db.refresh(confirmation_code)

    send_email(
        email=request.email,
        body=f'Ваш код подтверждения: {code}',
    )
    return request


@router_auth.post(
    '/signup-conformation/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
async def signup_conformation(
    request: schemas.ConfirmationCode, db: Session = Depends(get_db)
):
    confirmation_code = db.query(models.ConfirmationCode).filter(
        models.ConfirmationCode.email == request.email
    ).first()

    if confirmation_code.confirmation_code != request.confirmation_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'confirmation_code': 'Неверный код подтверждения'},
        )

    user_dict = request.dict()
    user_dict.pop('confirmation_code')
    password = user_dict.pop('password')
    new_user = models.User(**user_dict)
    new_user.password = hash_password(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
