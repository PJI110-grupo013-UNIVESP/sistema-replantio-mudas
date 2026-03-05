from fastapi import FastAPI

app = FastAPI(title="API Replantio de Mudas")

@app.get("/")
def read_root():
        return {"message": "API for the Seedling Replanting System is now operational!"}

@app.get("/status")
def status():
    return {"status": "OK", "Database": "Pending"}
