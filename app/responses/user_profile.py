from datetime import date, datetime
from app.responses.base import BaseResponse


class UserProfileResponse(BaseResponse):
    user_id: int
    first_name: str
    last_name: str
    dni: str
    phone: int
    address: str
    birth_date: date
    city: str
    zip_code: int
    

class UserProfileAdressResponse(BaseResponse):
    address: str
    city: str
    zip_code: int
    
class UserProfileDeleteResponse(BaseResponse):
    user_id: int
    first_name: str
    last_name: str
    dni: str
    phone: int
    address: str
    birth_date: date
    city: str
    zip_code: int
    deleted_at: datetime
    
    