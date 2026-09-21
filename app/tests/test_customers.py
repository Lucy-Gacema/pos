from tests.helpers import customer_payload

URL = "/customers/"


def test_create_customer(client, admin_headers):
    response = client.post(URL, json=customer_payload(), headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["customer_id"] > 0
    assert body["first_name"] == "John"
    assert body["phone_number"] == "+37061111111"
    assert body["points"] == 0


def test_last_name_email_and_points_are_optional(client, admin_headers):
    payload = {"first_name": "Solo", "phone_number": "555"}

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["last_name"] is None
    assert body["email"] is None
    assert body["points"] == 0


def test_two_customers_without_email_are_allowed(client, admin_headers):
    first = client.post(URL, json={"first_name": "A", "phone_number": "1"}, headers=admin_headers)
    second = client.post(URL, json={"first_name": "B", "phone_number": "2"}, headers=admin_headers)

    assert first.status_code == 201
    assert second.status_code == 201


def test_list_customers(client, admin_headers, customer):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_customer(client, admin_headers, customer):
    response = client.get(f"{URL}{customer['customer_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == customer


def test_update_customer_points(client, admin_headers, customer):
    response = client.put(
        f"{URL}{customer['customer_id']}", json={"points": 150}, headers=admin_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["points"] == 150
    assert body["first_name"] == "John"


def test_delete_customer(client, admin_headers, customer):
    response = client.delete(f"{URL}{customer['customer_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{customer['customer_id']}", headers=admin_headers).status_code == 404


def test_duplicate_phone_returns_409(client, admin_headers, customer):
    response = client.post(
        URL, json=customer_payload(email="other@example.com"), headers=admin_headers
    )

    assert response.status_code == 409


def test_duplicate_email_returns_409(client, admin_headers, customer):
    response = client.post(
        URL, json=customer_payload(phone_number="+37069999999"), headers=admin_headers
    )

    assert response.status_code == 409


def test_update_to_existing_phone_returns_409(client, admin_headers, customer):
    other = client.post(
        URL,
        json=customer_payload(phone_number="+37062222222", email="other@example.com"),
        headers=admin_headers,
    ).json()

    response = client.put(
        f"{URL}{other['customer_id']}",
        json={"phone_number": customer["phone_number"]},
        headers=admin_headers,
    )

    assert response.status_code == 409


def test_negative_points_returns_422(client, admin_headers):
    response = client.post(URL, json=customer_payload(points=-5), headers=admin_headers)

    assert response.status_code == 422


def test_invalid_email_returns_422(client, admin_headers):
    response = client.post(URL, json=customer_payload(email="bad-email"), headers=admin_headers)

    assert response.status_code == 422


def test_missing_first_name_returns_422(client, admin_headers):
    payload = customer_payload()
    del payload["first_name"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 422


def test_missing_phone_returns_422(client, admin_headers):
    payload = customer_payload()
    del payload["phone_number"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 422


def test_update_with_negative_points_returns_422(client, admin_headers, customer):
    response = client.put(
        f"{URL}{customer['customer_id']}", json={"points": -1}, headers=admin_headers
    )

    assert response.status_code == 422