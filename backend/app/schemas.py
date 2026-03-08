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
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
