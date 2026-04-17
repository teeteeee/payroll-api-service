"""Payroll service layer: business logic for employees and pay runs."""
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy.orm import Session

from app import models, schemas

TAX_RATE = Decimal("0.22")
CENTS = Decimal("0.01")


def _q(value: Decimal) -> Decimal:
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


def create_employee(db: Session, data: schemas.EmployeeCreate) -> models.Employee:
    emp = models.Employee(**data.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def list_employees(db: Session) -> list[models.Employee]:
    return db.query(models.Employee).order_by(models.Employee.id).all()


def get_employee(db: Session, employee_id: int) -> models.Employee | None:
    return db.get(models.Employee, employee_id)


def run_payroll(db: Session, data: schemas.PayRunCreate) -> models.PayRun:
    emp = get_employee(db, data.employee_id)
    if emp is None:
        raise ValueError("Employee not found")
    if data.period_end < data.period_start:
        raise ValueError("period_end must be >= period_start")

    gross = _q(Decimal(data.hours_worked) * Decimal(emp.hourly_rate))
    tax = _q(gross * TAX_RATE)
    net = _q(gross - tax)

    run = models.PayRun(
        employee_id=emp.id,
        period_start=data.period_start,
        period_end=data.period_end,
        hours_worked=data.hours_worked,
        gross_pay=gross,
        tax=tax,
        net_pay=net,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run
