from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserProfileRequest(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    dni: str
    phone: int
    address: str
    birth_date: date
    city: str
    zip_code: int
    
class UserProfileUpdateRequest(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    dni: str
    phone: int
    address: str
    birth_date: date
    city: str
    zip_code: int
    

class UserProfileUpdateAdressRequest(BaseModel):
    address: str
    city: str
    zip_code: int