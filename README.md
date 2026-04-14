# Module 11 — Calculation Model with Polymorphism & Factory Pattern

**GitHub:** https://github.com/KKS071/assignment11_calculation_model  
**Docker Hub:** https://hub.docker.com/r/kks59/601_module11

---

## Project Overview

This project implements a **FastAPI calculator** backed by:

- **SQLAlchemy polymorphic models** — `Addition`, `Subtraction`, `Multiplication`, and `Division` all inherit from a shared `Calculation` base stored in one `calculations` table (single-table inheritance).
- **Pydantic v2 schemas** — validate and serialize all API input/output with custom field and model validators.
- **Factory pattern** — `Calculation.create(type, user_id, inputs)` returns the correct subclass without the caller needing to import individual classes.
- **FastAPI endpoints** — `/add`, `/subtract`, `/multiply`, `/divide` with proper error handling.
- **Playwright E2E tests**, **integration tests**, and **unit tests** targeting 100% coverage.

### How polymorphism works here

The `Calculation` base class is mapped to the `calculations` table with `polymorphic_on="type"`. Each subclass (`Addition`, `Subtraction`, etc.) sets its own `polymorphic_identity`. When SQLAlchemy loads a row it reads the `type` column and automatically returns the correct subclass instance. Every subclass overrides `get_result()` with its own logic, so calling `calc.get_result()` always does the right thing regardless of which subclass you have.

### How the factory pattern works here

`Calculation.create(calculation_type, user_id, inputs)` is a classmethod that maps type strings to subclass constructors and returns the matching instance. Adding a new operation type only requires a new subclass and one dict entry — nothing else changes.

---

## How to Run the App

### Local

```bash
git clone https://github.com/KKS071/assignment11_calculation_model.git
cd assignment11_calculation_model

python3 -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate.bat   # Windows

pip install -r requirements.txt
python main.py
```

App is available at `http://127.0.0.1:8000`.

### Docker

```bash
# Pull from Docker Hub
docker pull kks59/601_module11

# Run the container
docker run -p 8000:8000 kks59/601_module11
```

### Build locally with Docker

```bash
docker build -t module11 .
docker run -p 8000:8000 module11
```

---

## How to Run Tests

### All tests with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Unit tests only

```bash
pytest tests/unit/
```

### Integration tests only

```bash
pytest tests/integration/
```

### Integration tests with a live PostgreSQL container

```bash
docker-compose up -d db
pytest tests/integration/
docker-compose down
```

### E2E tests (Playwright)

```bash
# Install Playwright browsers (one-time setup)
playwright install chromium

# Run E2E tests
pytest -m e2e
```

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/`) runs automatically on every push to `main`:

1. Starts a PostgreSQL service container for integration tests.
2. Installs Python dependencies and Playwright browsers.
3. Runs the full test suite with `pytest --cov`.
4. On success, builds the Docker image and pushes it to Docker Hub as `kks59/601_module11`.

Docker Hub credentials are stored as GitHub repository secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`).

---

## Module 11 Requirements Summary

| Requirement | File(s) |
|---|---|
| SQLAlchemy polymorphic model | `app/models/calculation.py` |
| User model | `app/models/user.py` |
| Pydantic schemas | `app/schemas/calculation.py` |
| Factory pattern | `Calculation.create()` in `app/models/calculation.py` |
| Database config | `app/database.py`, `app/core/config.py` |
| FastAPI app & routes | `main.py` |
| Frontend template | `templates/index.html` |
| Unit tests | `tests/unit/test_calculator.py` |
| Integration tests | `tests/integration/test_calculation.py` |
| Schema tests | `tests/integration/test_calculation_schema.py` |
| API tests | `tests/integration/test_fastapi_calculator.py` |
| E2E tests | `tests/e2e/test_e2e.py` |
| Test fixtures | `tests/conftest.py` |
| CI/CD | `.github/workflows/` |

---

## Useful Commands

| Action | Command |
|---|---|
| Run app locally | `python main.py` |
| Pull Docker image | `docker pull kks59/601_module11` |
| Run Docker container | `docker run -p 8000:8000 kks59/601_module11` |
| Run all tests | `pytest` |
| Run tests with coverage | `pytest --cov=app --cov-report=term-missing` |
| Run E2E tests | `pytest -m e2e` |
| Install Playwright browsers | `playwright install chromium` |

---

## Links

- **GitHub Repository:** https://github.com/KKS071/assignment11_calculation_model
- **Docker Hub Image:** https://hub.docker.com/r/kks59/601_module11
