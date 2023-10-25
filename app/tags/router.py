from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from core.database import get_db
from core.db_utils import check_if_already_registered

router_tags = APIRouter()


@router_tags.get(
    '/', status_code=status.HTTP_200_OK,
    response_model=List[schemas.Tag],
)
async def get_tags(limit: int = 10, db: Session = Depends(get_db)):
    tags = db.query(models.Tag).limit(limit).all()
    return tags


@router_tags.get(
    '/{tag_id}/', status_code=status.HTTP_200_OK,
    response_model=schemas.Tag,
)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'tag': 'Тег не найден'},
        )
    return tag


@router_tags.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=schemas.Tag,
)
async def create_tag(request: schemas.Tag, db: Session = Depends(get_db)):
    check_if_already_registered(models.Tag, 'name', request.name, db)
    check_if_already_registered(models.Tag, 'slug', request.slug, db)

    new_tag = models.Tag(**request.dict())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag
