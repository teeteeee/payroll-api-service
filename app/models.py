"""SQLAlchemy ORM models for payroll domain."""
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hourly_rate = Column(Numeric(10, 2), nullable=False)

    payruns = relationship("PayRun", back_populates="employee", cascade="all, delete-orphan")


class PayRun(Base):
    __tablename__ = "payruns"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    hours_worked = Column(Numeric(10, 2), nullable=False)
    gross_pay = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    net_pay = Column(Numeric(10, 2), nullable=False)

    employee = relationship("Employee", back_populates="payruns")
