from pydantic import BaseModel
from typing import Optional, List

# Pydantic models
class MascotCreate(BaseModel):
    name:str
    race:str
    sku:str
    picture:str
    available:str

class MascotResponse(BaseModel):
    id:int
    name:str
    sku:str
    picture:str
    race:str
    available:str

    class Config:
        from_attributes = True

class MascotUpdate(BaseModel):
    name:Optional[str] = None
    race:Optional[str] = None
    sku:Optional[str] = None
    picture:Optional[str] = None
    available:Optional[str] = None

