from decimal import Decimal

from app.core.security import create_access_token, hash_password
from app.models.users import User

DEFAULT_PASSWORD = "password123"


def dec(value) -> Decimal:
    return Decimal(str(value))


def auth_headers_for(user) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user.user_id)}"}


def create_user_in_db(session, username, role="cashier", is_active=True,
                      password=DEFAULT_PASSWORD):
    user = User(
        username=username,
        password_hash=hash_password(password),
        first_name="Test",
        last_name="User",
        role=role,
        is_active=is_active,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_ok(client, url, payload, headers):
    response = client.post(url, json=payload, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()


def user_payload(**overrides):
    return {
        "username": "newuser",
        "password": DEFAULT_PASSWORD,
        "first_name": "New",
        "last_name": "User",
        "role": "cashier",
        **overrides,
    }


def category_payload(**overrides):
    return {"category_name": "Drinks", "is_active": True, **overrides}


def supplier_payload(**overrides):
    return {
        "company_name": "Acme Ltd",
        "contact_name": "Jane Doe",
        "phone_number": "+37060000000",
        "email": "acme@example.com",
        "address": "1 Main Street",
        "is_active": True,
        **overrides,
    }


def customer_payload(**overrides):
    return {
        "first_name": "John",
        "last_name": "Smith",
        "phone_number": "+37061111111",
        "email": "john@example.com",
        "points": 0,
        **overrides,
    }


def product_payload(category_id, supplier_id, **overrides):
    return {
        "product_name": "Cola",
        "barcode": "5449000000096",
        "category_id": category_id,
        "selling_price": "1.99",
        "reorder_level": 10,
        "in_stock": 100,
        "supplier_id": supplier_id,
        **overrides,
    }


def receipt_payload(**overrides):
    return {"receipt_number": "R-0001", "is_printed": False, **overrides}


def sale_payload(user_id, receipt_number, **overrides):
    return {
        "user_id": user_id,
        "customer_id": None,
        "total_amount": "10.00",
        "discount_amount": "0.00",
        "tax_amount": "2.10",
        "payment_status": "paid",
        "receipt_number": receipt_number,
        "sale_date": "2026-01-15T10:30:00",
        **overrides,
    }


def sale_item_payload(sale_id, product_id, **overrides):
    return {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "unit_price": "1.99",
        **overrides,
    }


def payment_payload(sale_id, **overrides):
    return {
        "sale_id": sale_id,
        "payment_method": "cash",
        "amount_paid": "10.00",
        "payment_date": "2026-01-15T10:31:00",
        **overrides,
    }
