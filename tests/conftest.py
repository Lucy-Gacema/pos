import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, engine as app_engine, get_db
from app.main import app
from tests.helpers import (
    auth_headers_for,
    category_payload,
    create_ok,
    create_user_in_db,
    customer_payload,
    product_payload,
    receipt_payload,
    sale_payload,
    supplier_payload,
)

assert app_engine.url.get_backend_name() == "sqlite", (
    "Tests must only ever run against SQLite"
)

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(test_engine, "connect")
def _enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autoflush=False, bind=test_engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    return create_user_in_db(db_session, "admin", role="admin")


@pytest.fixture
def cashier_user(db_session):
    return create_user_in_db(db_session, "cashier", role="cashier")


@pytest.fixture
def admin_headers(admin_user):
    return auth_headers_for(admin_user)


@pytest.fixture
def cashier_headers(cashier_user):
    return auth_headers_for(cashier_user)


@pytest.fixture
def auth_headers(admin_headers):
    return admin_headers


@pytest.fixture
def category(client, admin_headers):
    return create_ok(client, "/categories/", category_payload(), admin_headers)


@pytest.fixture
def supplier(client, admin_headers):
    return create_ok(client, "/suppliers/", supplier_payload(), admin_headers)


@pytest.fixture
def product(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"])
    return create_ok(client, "/products/", payload, admin_headers)


@pytest.fixture
def customer(client, admin_headers):
    return create_ok(client, "/customers/", customer_payload(), admin_headers)


@pytest.fixture
def receipt(client, admin_headers):
    return create_ok(client, "/receipts/", receipt_payload(), admin_headers)


@pytest.fixture
def sale(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"])
    return create_ok(client, "/sales/", payload, admin_headers)
