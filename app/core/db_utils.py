from getpass import getpass
from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

from .database import SessionLocal
from .hashing import hash_password
from users import models, schemas

db = SessionLocal()

fields_names = {
    'username': 'Имя пользователя',
    'email': 'Адрес электронной почты',
}


def check_if_already_registered(
            model: BaseModel, field_name: str,
            field_value: Any, db: Session
        ) -> None:

    filter_criteria = {field_name: field_value}
    ru_field_name = fields_names.get(field_name, field_name)
    if db.query(model).filter_by(**filter_criteria).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={f'{field_name}': f'{ru_field_name} уже зарегистрирован'},
        )


def create_superuser() -> str:
    """
    Create a super user with the given username, email, and password.

    Returns:
        str: A message confirming the successful creation of the superuser.
    """
    username = input('Введите имя пользователя: ')

    if db.query(models.User).filter(models.User.username == username).first():
        return f'Пользователь {username} уже существует'

    email = input('Введите адрес электронной почты: ')

    if db.query(models.User).filter(models.User.email == email).first():
        return f'Пользователь c {email} уже существует'

    password = getpass('Введите пароль: ')

    try:
        schemas.BaseUser(username=username, email=email, password=password)
    except ValidationError as e:
        return e

    password = hash_password(password)
    new_user = models.User(username=username, email=email,
                           password=password, is_superuser=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return 'Superuser успешно создан!'
