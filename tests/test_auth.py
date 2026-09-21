from datetime import datetime, timedelta, timezone

import jwt

from app.core import security
from app.core.security import decode_access_token
from tests.helpers import DEFAULT_PASSWORD, auth_headers_for, create_user_in_db, user_payload


def register(client, **overrides):
    payload = user_payload(**overrides)
    payload.pop("role", None)
    return client.post("/auth/register", json=payload)


def test_first_registered_user_becomes_admin(client):
    response = register(client, username="alice")

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "alice"
    assert body["role"] == "admin"
    assert body["is_active"] is True


def test_later_users_register_as_cashier(client):
    register(client, username="alice")

    response = register(client, username="bob")

    assert response.status_code == 201
    assert response.json()["role"] == "cashier"


def test_register_cannot_choose_a_role(client):
    register(client, username="alice")

    response = client.post(
        "/auth/register",
        json={**user_payload(username="mallory"), "role": "admin"},
    )

    assert response.status_code == 201
    assert response.json()["role"] == "cashier"


def test_register_never_returns_password_data(client):
    body = register(client, username="alice").json()

    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_username_returns_409(client):
    register(client, username="alice")

    response = register(client, username="alice")

    assert response.status_code == 409


def test_register_short_password_returns_422(client):
    response = register(client, password="short")

    assert response.status_code == 422


def test_register_short_username_returns_422(client):
    response = register(client, username="ab")

    assert response.status_code == 422


def test_register_missing_fields_returns_422(client):
    response = client.post("/auth/register", json={"username": "alice"})

    assert response.status_code == 422


def test_login_success_returns_working_token(client):
    register(client, username="alice")

    response = client.post(
        "/auth/login", json={"username": "alice", "password": DEFAULT_PASSWORD}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert decode_access_token(body["access_token"])["sub"].isdigit()

    protected = client.get(
        "/categories/", headers={"Authorization": f"Bearer {body['access_token']}"}
    )
    assert protected.status_code == 200


def test_login_wrong_password_returns_401(client):
    register(client, username="alice")

    response = client.post(
        "/auth/login", json={"username": "alice", "password": "wrong-password"}
    )

    assert response.status_code == 401


def test_login_unknown_user_returns_401(client):
    response = client.post(
        "/auth/login", json={"username": "ghost", "password": DEFAULT_PASSWORD}
    )

    assert response.status_code == 401


def test_login_error_does_not_reveal_which_part_was_wrong(client):
    register(client, username="alice")

    wrong_password = client.post(
        "/auth/login", json={"username": "alice", "password": "wrong-password"}
    )
    unknown_user = client.post(
        "/auth/login", json={"username": "ghost", "password": "wrong-password"}
    )

    assert wrong_password.json() == unknown_user.json()


def test_login_inactive_user_returns_400(client, db_session):
    create_user_in_db(db_session, "sleepy", is_active=False)

    response = client.post(
        "/auth/login", json={"username": "sleepy", "password": DEFAULT_PASSWORD}
    )

    assert response.status_code == 400


def test_login_missing_fields_returns_422(client):
    response = client.post("/auth/login", json={"username": "alice"})

    assert response.status_code == 422


def test_missing_token_returns_401(client):
    response = client.get("/categories/")

    assert response.status_code == 401


def test_malformed_token_returns_401(client):
    response = client.get("/categories/", headers={"Authorization": "Bearer nonsense"})

    assert response.status_code == 401


def test_wrong_auth_scheme_returns_401(client, admin_user):
    token = auth_headers_for(admin_user)["Authorization"].split(" ")[1]

    response = client.get("/categories/", headers={"Authorization": f"Basic {token}"})

    assert response.status_code == 401


def test_expired_token_returns_401(client, admin_user):
    expired = jwt.encode(
        {
            "sub": str(admin_user.user_id),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        security.jwt_secret,
        algorithm=security.jwt_algorithm,
    )

    response = client.get("/categories/", headers={"Authorization": f"Bearer {expired}"})

    assert response.status_code == 401


def test_token_with_non_numeric_subject_returns_401(client):
    token = jwt.encode(
        {"sub": "abc", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        security.jwt_secret,
        algorithm=security.jwt_algorithm,
    )

    response = client.get("/categories/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_token_for_deleted_user_returns_401(client):
    from app.core.security import create_access_token

    token = create_access_token(9999)

    response = client.get("/categories/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401


def test_token_for_deactivated_user_returns_401(client, db_session):
    user = create_user_in_db(db_session, "sleepy", is_active=False)

    response = client.get("/categories/", headers=auth_headers_for(user))

    assert response.status_code == 401
