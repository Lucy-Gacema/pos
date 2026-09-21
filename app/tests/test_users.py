from tests.helpers import DEFAULT_PASSWORD, user_payload

URL = "/users/"


def test_admin_can_create_user(client, admin_headers):
    response = client.post(URL, json=user_payload(), headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["user_id"] > 0
    assert body["username"] == "newuser"
    assert body["role"] == "cashier"
    assert body["is_active"] is True
    assert "password" not in body
    assert "password_hash" not in body


def test_admin_can_create_admin(client, admin_headers):
    response = client.post(
        URL, json=user_payload(username="boss", role="admin"), headers=admin_headers
    )

    assert response.status_code == 201
    assert response.json()["role"] == "admin"


def test_role_defaults_to_cashier(client, admin_headers):
    payload = user_payload()
    del payload["role"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    assert response.json()["role"] == "cashier"


def test_list_users(client, admin_headers, admin_user):
    client.post(URL, json=user_payload(), headers=admin_headers)

    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    usernames = [u["username"] for u in response.json()]
    assert usernames == ["admin", "newuser"]


def test_get_user(client, admin_headers, admin_user):
    response = client.get(f"{URL}{admin_user.user_id}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_update_user(client, admin_headers):
    created = client.post(URL, json=user_payload(), headers=admin_headers).json()

    response = client.put(
        f"{URL}{created['user_id']}",
        json={"first_name": "Changed", "is_active": False},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["first_name"] == "Changed"
    assert body["is_active"] is False
    assert body["last_name"] == "User"  # untouched field is preserved


def test_update_password_changes_login(client, admin_headers):
    created = client.post(URL, json=user_payload(), headers=admin_headers).json()

    client.put(
        f"{URL}{created['user_id']}",
        json={"password": "brand-new-password"},
        headers=admin_headers,
    )

    old = client.post(
        "/auth/login", json={"username": "newuser", "password": DEFAULT_PASSWORD}
    )
    new = client.post(
        "/auth/login", json={"username": "newuser", "password": "brand-new-password"}
    )
    assert old.status_code == 401
    assert new.status_code == 200


def test_delete_user(client, admin_headers):
    created = client.post(URL, json=user_payload(), headers=admin_headers).json()

    response = client.delete(f"{URL}{created['user_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{created['user_id']}", headers=admin_headers).status_code == 404



def test_duplicate_username_returns_409(client, admin_headers):
    client.post(URL, json=user_payload(), headers=admin_headers)

    response = client.post(URL, json=user_payload(), headers=admin_headers)

    assert response.status_code == 409


def test_update_to_existing_username_returns_409(client, admin_headers):
    client.post(URL, json=user_payload(username="first"), headers=admin_headers)
    second = client.post(URL, json=user_payload(username="second"), headers=admin_headers).json()

    response = client.put(
        f"{URL}{second['user_id']}", json={"username": "first"}, headers=admin_headers
    )

    assert response.status_code == 409


def test_invalid_role_returns_422(client, admin_headers):
    response = client.post(
        URL, json=user_payload(role="superuser"), headers=admin_headers
    )

    assert response.status_code == 422


def test_short_password_returns_422(client, admin_headers):
    response = client.post(URL, json=user_payload(password="short"), headers=admin_headers)

    assert response.status_code == 422


def test_missing_username_returns_422(client, admin_headers):
    payload = user_payload()
    del payload["username"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 422


def test_update_with_invalid_role_returns_422(client, admin_headers, admin_user):
    response = client.put(
        f"{URL}{admin_user.user_id}", json={"role": "superuser"}, headers=admin_headers
    )

    assert response.status_code == 422



def test_cashier_cannot_manage_users(client, cashier_headers, admin_user):
    user_url = f"{URL}{admin_user.user_id}"

    assert client.get(URL, headers=cashier_headers).status_code == 403
    assert client.get(user_url, headers=cashier_headers).status_code == 403
    assert client.post(URL, json=user_payload(), headers=cashier_headers).status_code == 403
    assert client.put(user_url, json={"role": "cashier"}, headers=cashier_headers).status_code == 403
    assert client.delete(user_url, headers=cashier_headers).status_code == 403


def test_cashier_cannot_promote_themselves(client, cashier_headers, cashier_user):
    response = client.put(
        f"{URL}{cashier_user.user_id}", json={"role": "admin"}, headers=cashier_headers
    )

    assert response.status_code == 403


def test_users_require_authentication(client):
    assert client.get(URL).status_code == 401
    assert client.post(URL, json=user_payload()).status_code == 401