from pydantic import BaseModel
from datetime import date
from typing import Optional


class MudaBase(BaseModel):
    species: str
    batch: str
    supplier: str
    amount: int


class MudaCreate(MudaBase):
    pass


class MudaResponse(MudaBase):
    id: int
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "common"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    is_active: bool
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class ReplantioBase(BaseModel):
    muda_id: int
    area_name: str
    amount: int
    status: str = "Planejado"
    planned_date: Optional[date] = None
    actual_date: Optional[date] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    surviving_amount: Optional[int] = None


class ReplantioCreate(ReplantioBase):
    pass


class ReplantioResponse(ReplantioBase):
    id: int
    user_id: int
    model_config = {"from_attributes": True}
