from datetime import datetime

from pydantic import ConfigDict
from app.responses.base import BaseResponse

class CategoryResponse(BaseResponse):
    id: int
    name: str
    description: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdateResponse(BaseResponse):
    id: int
    name: str
    description: str
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CategoryDeleteResponse(BaseResponse):
    id: int
    name: str
    description: str
    deleted_at: datetime

    model_config = ConfigDict(from_attributes=True)
