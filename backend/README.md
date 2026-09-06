# Education Center CRM - Backend Architecture

Python backend architecture structured for future REST / GraphQL API expansion and SQLite local development.

## Tech Stack
- **FastAPI**: Modern, high-performance web framework
- **SQLAlchemy 2.0**: Type-safe ORM
- **SQLite**: Zero-configuration embedded database for local development
- **Pydantic v2**: Data validation and serialization

## Quickstart

```bash
# Create virtual environment
python -m venv .venv

# Activate environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m backend.app.main
```

The API health check will be accessible at: `http://127.0.0.1:8000/api/health`
API documentation (Swagger UI) at: `http://127.0.0.1:8000/docs`
