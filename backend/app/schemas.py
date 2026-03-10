from pydantic import BaseModel


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
