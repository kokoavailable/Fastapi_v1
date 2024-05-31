from pydantic import BaseModel
from typing import Optional, Any

class ResponseModel(BaseModel):
    status: str
    code: int
    message: Optional[str] = None
    data: Optional[Any] = None