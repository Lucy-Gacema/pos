# POS Backend

A point-of-sale REST API built with FastAPI, SQLAlchemy and PostgreSQL.
It manages categories, suppliers, products, customers, users, sales, sale items,
payments and receipts, with JWT authentication.

## Install dependencies

```bash
python -m venv venv
source venv/bin/activate      
pip install -r requirements.txt
```

## Run the backend locally

1. Copy `.env.example` to `.env` and set `DATABASE_URL` (your PostgreSQL database),
   `JWT_SECRET` and `JWT_ALGORITHM`.
2. Start the server:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Open http://127.0.0.1:8000/docs for the interactive API documentation.

The first account created with `POST /auth/register` becomes the **admin**; later
sign-ups are **cashiers**. Only admins can manage users or delete records.

## Run the tests

```bash
pytest
```

The tests use an **in-memory SQLite database** and never connect to PostgreSQL:
`tests/conftest.py` forces `DATABASE_URL=sqlite://` before the app is imported and
replaces the `get_db` dependency with a SQLite session. A fresh empty database is
created for every test, so running `pytest` cannot read, change or delete your
development data.

Tests live in `tests/` (one `test_<entity>.py` per entity, plus authentication and
authorization tests). They run automatically on every push and pull request through
GitHub Actions (`.github/workflows/tests.yml`).