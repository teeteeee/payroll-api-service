"""Pay runs router."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import payroll_service

router = APIRouter(prefix="/payruns", tags=["payruns"])


@router.post("/", response_model=schemas.PayRunOut, status_code=status.HTTP_201_CREATED)
def create_payrun(data: schemas.PayRunCreate, db: Session = Depends(get_db)):
    try:
        return payroll_service.run_payroll(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
