"""Payroll API Service - FastAPI entrypoint."""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import employees, payruns

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payroll API Service",
    description="Secure, containerized REST API for payroll processing.",
    version="0.1.0",
)

app.include_router(employees.router)
app.include_router(payruns.router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
