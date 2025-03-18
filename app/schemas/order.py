from typing import List, Optional
from pydantic import BaseModel


class ProductOrderRequest(BaseModel):
    product_id: int  
    quantity: int    

class CreateOrderRequest(BaseModel):
    user_id: int                 
    products: List[ProductOrderRequest]  
    
class OrderStatusUpdateRequest(BaseModel):
    status: Optional[str]  

