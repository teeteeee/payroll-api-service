"""Pydantic schemas for request/response validation."""
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    hourly_rate: Decimal = Field(..., gt=0)


class EmployeeOut(EmployeeCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PayRunCreate(BaseModel):
    employee_id: int
    period_start: date
    period_end: date
    hours_worked: Decimal = Field(..., ge=0)


class PayRunOut(BaseModel):
    id: int
    employee_id: int
    period_start: date
    period_end: date
    hours_worked: Decimal
    gross_pay: Decimal
    tax: Decimal
    net_pay: Decimal
    model_config = ConfigDict(from_attributes=True)
