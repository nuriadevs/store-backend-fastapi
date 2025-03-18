from pydantic import BaseModel, ConfigDict

class CategoryCreateRequest(BaseModel):   
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class CategoryDeleteRequest(BaseModel):   
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

