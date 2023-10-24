from typing import Any

from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


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
