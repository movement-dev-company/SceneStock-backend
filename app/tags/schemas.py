from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str = Field(max_length=64, min_length=3)
    slug: str = Field(max_length=64, min_length=3)

    class Config:
        orm_mode = True
