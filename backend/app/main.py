from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Replantio de Mudas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=("*"),  # Aqui vai a URL quando estiver em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message":
            "API for the Seedling Replanting System is now operational!"
            }


@app.get("/status")
def status():
    return {"status": "Online",
            "Database": "Conectado",
            "Mudas_Cadastradas": 3000
            }
