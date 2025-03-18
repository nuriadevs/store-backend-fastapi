from typing import List, Optional
from datetime import datetime
from app.responses.base import BaseResponse


class OrderItemResponse(BaseResponse):
    product_id: int
    name: Optional[str] 
    quantity: int
    subtotal: float


class OrderResponse(BaseResponse):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemResponse] 



class OrderDeleteResponse(BaseResponse):
    id: int
    user_id: int
    total_price: float
    status: str

    order_items: List[OrderItemResponse] 
    deleted_at:datetime