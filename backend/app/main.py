from fastapi import FastAPI, Depends, HTTPException
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


@app.put("/mudas/{muda_id}", response_model=MudaResponse)
def update_item(muda_id: int,
                muda_updated: MudaCreate,
                db: Session = Depends(get_db)):
    item = db.query(models.Muda).filter(models.Muda.id == muda_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.species = muda_updated.species
    item.supplier = muda_updated.supplier
    item.amount = muda_updated.amount
    item.batch = muda_updated.batch

    db.commit()
    db.refresh(item)
    return item


@app.delete("/mudas/{muda_id}")
def delete_item(muda_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Muda).filter(models.Muda.id == muda_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item successfully deleted."}


@app.get("/status")
def status():
    return {"status": "Online",
            "Database": "Conectado",
            "Mudas_Cadastradas": 3000
            }
