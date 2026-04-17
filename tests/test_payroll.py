"""Integration tests for the Payroll API."""
import os
import tempfile
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

# Use an isolated sqlite DB for tests
_fd, _path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_path}"

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_employee_and_run_payroll():
    r = client.post(
        "/employees/",
        json={"full_name": "Jane Doe", "email": "jane@example.com", "hourly_rate": "50.00"},
    )
    assert r.status_code == 201
    emp = r.json()

    r = client.post(
        "/payruns/",
        json={
            "employee_id": emp["id"],
            "period_start": "2026-04-01",
            "period_end": "2026-04-15",
            "hours_worked": "80",
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert Decimal(body["gross_pay"]) == Decimal("4000.00")
    assert Decimal(body["tax"]) == Decimal("880.00")
    assert Decimal(body["net_pay"]) == Decimal("3120.00")


def test_payrun_missing_employee_returns_400():
    r = client.post(
        "/payruns/",
        json={
            "employee_id": 99999,
            "period_start": "2026-04-01",
            "period_end": "2026-04-15",
            "hours_worked": "10",
        },
    )
    assert r.status_code == 400
