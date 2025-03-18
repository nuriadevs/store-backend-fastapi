from decimal import Decimal
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ProductCreateRequest(BaseModel):   
    name: str
    description: str
    price: Decimal
    stock: int
    category_id: int


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = Field(None)

class ProductResponseRequest(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime