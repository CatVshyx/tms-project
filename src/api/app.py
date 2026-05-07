from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="TMS API", version="1.0.0")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TMS",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@app.get("/tasks")
def get_tasks():
    return {"tasks": [], "total": 0}
