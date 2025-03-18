
from decimal import Decimal
from app.responses.base import BaseResponse

class ProductResponse(BaseResponse):
    name: str
    description: str
    price: Decimal
    stock: int
    category_id: int