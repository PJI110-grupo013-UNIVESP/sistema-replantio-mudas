from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
import os
from dotenv import load_dotenv

from . import models, schemas, auth
from .database import engine, get_db, SessionLocal

load_dotenv()

models.Base.metadata.create_all(bind=engine)


def admin_default():
    db = SessionLocal()
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    user_exists = db.query(models.User).filter(
        models.User.email == admin_email).first()

    if not user_exists:
        print(f"Creating a default administrator user: {admin_email}")
        passwd_encryp = auth.get_password_hash(admin_password)  # type: ignore
        new_admin = models.User(
            name='Administrator',
            email=admin_email,
            hashed_password=passwd_encryp,
            role="admin"
        )
        db.add(new_admin)
        db.commit()

    db.close()


admin_default()

app = FastAPI(title="API Replantio de Mudas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Alterar em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SEGURAÇA DA APLICAÇÃO ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))  # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="We were unable to validate the login credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM])  # type: ignore
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- ROTAS DE UTILIZADORES E AUTENTICAÇÃO ---


@app.get("/users", response_model=list[schemas.UserResponse])
def list_user(db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only administrators can view users."
        )
    return db.query(models.User).all()


@app.post("/users", response_model=schemas.UserResponse,
          status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Access denied. Only administrators")

    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registado")

    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied.")

    user_to_delete = db.query(models.User).filter(
        models.User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=404, detail="User not found.")

    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=400, detail="Você não pode excluir sua própria conta.")

    db.delete(user_to_delete)
    db.commit()
    return {"message": "User successfully deleted."}


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == form_data.username).first()

    if not user or not auth.verify_password(form_data.password,
                                            user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou palavra-passe incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTAS DE MUDAS ---


@app.get("/")
def read_root():
    return {
        "message":
        "API for the Seedling Replanting System is now operational!"

    }


@app.get("/mudas", response_model=list[schemas.MudaResponse])
def list_items(db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    return db.query(models.Muda).all()


@app.post("/mudas", response_model=schemas.MudaResponse)
def create_items(muda: schemas.MudaCreate,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):
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


@app.put("/mudas/{muda_id}", response_model=schemas.MudaResponse)
def update_item(muda_id: int, muda_updated: schemas.MudaCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
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
def delete_item(muda_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Muda).filter(models.Muda.id == muda_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item successfully deleted."}


@app.get("/status")
def status_api():
    return {"status": "Online", "Database": "Conectado"}
