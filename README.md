# payroll-api-service

A secure, containerized REST API for payroll processing. Built with Python (FastAPI), PostgreSQL, Docker, and GitHub Actions CI/CD. Includes Pytest coverage and a service-layer architecture.

## Features

- **FastAPI** REST API with auto-generated OpenAPI docs at `/docs`
- **PostgreSQL** persistence via SQLAlchemy
- **Service-layer architecture** separating HTTP routers, business logic (services), and data models
- **Pytest** test suite with coverage reporting
- **Dockerfile** and **docker-compose** for reproducible local development
- **GitHub Actions** CI: runs tests against a Postgres service and builds the Docker image

## Project structure

```
app/
  main.py              # FastAPI app factory
  database.py          # SQLAlchemy engine/session
  models.py            # ORM models (Employee, PayRun)
  schemas.py           # Pydantic schemas
  routers/             # HTTP routers (employees, payruns)
  services/            # Business logic (payroll_service)
tests/                 # Pytest integration tests
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

## Quick start (Docker Compose)

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` and interactive docs at `http://localhost:8000/docs`.

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://payroll:payroll@localhost:5432/payroll
uvicorn app.main:app --reload
```

## Running tests

```bash
pip install pytest pytest-cov
pytest --cov=app --cov-report=term-missing
```

## API endpoints

- `GET  /health` — health check
- `POST /employees` — create employee
- `GET  /employees` — list employees
- `GET  /employees/{id}` — get employee
- `POST /payruns` — run payroll for a period
- `GET  /payruns` — list pay runs

## CI/CD

Every push and pull request against `main` runs the GitHub Actions workflow defined in `.github/workflows/ci.yml`, which:

1. Spins up a Postgres 15 service container
2. Installs dependencies and runs `pytest` with coverage
3. Builds the production Docker image

## License

MIT — see [LICENSE](./LICENSE).
