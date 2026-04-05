import app.config

from fastapi import FastAPI
from app.api import documents, query

app = FastAPI()

app.include_router(documents.router)
app.include_router(query.router)

@app.get("/")
def root():
    return {"message": "Insightify Lite API running"}