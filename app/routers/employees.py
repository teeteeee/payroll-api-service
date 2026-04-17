"""Employees router."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import payroll_service

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(data: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return payroll_service.create_employee(db, data)


@router.get("/", response_model=list[schemas.EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    return payroll_service.list_employees(db)


@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = payroll_service.get_employee(db, employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp
