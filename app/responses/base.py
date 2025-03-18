from pydantic import BaseModel, ConfigDict

class BaseResponse(BaseModel):
    """
    Clase base para las respuestas de la API.
    """
    model_config = ConfigDict(from_attributes=True, arbitrary_type_allowed=True)