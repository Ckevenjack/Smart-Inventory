from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services import stats_service

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return stats_service.get_stats(db)