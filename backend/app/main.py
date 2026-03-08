from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Replantio de Mudas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aqui vai a URL quando estiver em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MudaBase(BaseModel):
    species: str
    batch: str
    supplier: str
    amount: int


class MudaResponse(MudaBase):
    id: int

    class Config:
        from_attributes = True


class MudaCreate(MudaBase):
    pass


@app.get("/")
def read_root():
    return {"message":
            "API for the Seedling Replanting System is now operational!"
            }


@app.get("/mudas", response_model=list[MudaResponse])
def list_items(db: Session = Depends(get_db)):
    mudas = db.query(models.Muda).all()
    return mudas


@app.post("/mudas", response_model=MudaResponse)
def create_items(muda: MudaCreate, db: Session = Depends(get_db)):
    new_item = models.Muda(
        species=muda.species,
        batch=muda.batch,
        supplier=muda.supplier,
        amount=muda.amount
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/status")
def status():
    return {"status": "Online",
            "Database": "Conectado",
            "Mudas_Cadastradas": 3000
            }
