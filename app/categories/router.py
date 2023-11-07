from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from core.database import get_db
from core.db_utils import check_if_already_registered

router_categories = APIRouter()


@router_categories.get(
    '/', status_code=status.HTTP_200_OK,
    response_model=List[schemas.Category],
)
async def get_categories(limit: int = 10, db: Session = Depends(get_db)):
    categories = await db.query(models.Categories).limit(limit).all()
    return categories


@router_categories.get(
    '/{category_id}/', status_code=status.HTTP_200_OK,
    response_model=schemas.Category,
)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    category = await db.query(models.Categories).filter(
        models.Categories.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'category': 'Категория не найдена'},
        )
    return category


@router_categories.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=schemas.Category,
)
async def create_category(
        request: schemas.Category, db: Session = Depends(get_db)):
    check_if_already_registered(models.Categories, 'name', request.name, db)
    check_if_already_registered(models.Categories, 'slug', request.slug, db)

    new_category = models.Categories(**request.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return await new_category
