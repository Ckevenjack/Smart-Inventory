from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.routers.products import router as product_router
from app.routers.stats import router as stats_router

from app.database import get_db

from app.services import stats_service

app = FastAPI()

app.include_router(product_router)
app.include_router(stats_router)

@app.get("/")
def home_page():
    return {"message": "Smart Inventory API"}
