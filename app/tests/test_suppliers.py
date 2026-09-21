from tests.helpers import supplier_payload

URL = "/suppliers/"


def test_create_supplier(client, admin_headers):
    response = client.post(URL, json=supplier_payload(), headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["supplier_id"] > 0
    assert body["company_name"] == "Acme Ltd"
    assert body["email"] == "acme@example.com"
    assert body["is_active"] is True


def test_optional_fields_can_be_omitted(client, admin_headers):
    payload = {"company_name": "Bare Co", "contact_name": "Bob", "phone_number": "123"}

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] is None
    assert body["address"] is None
    assert body["is_active"] is True


def test_list_suppliers(client, admin_headers, supplier):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_supplier(client, admin_headers, supplier):
    response = client.get(f"{URL}{supplier['supplier_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == supplier


def test_update_supplier(client, admin_headers, supplier):
    response = client.put(
        f"{URL}{supplier['supplier_id']}",
        json={"contact_name": "New Contact", "is_active": False},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["contact_name"] == "New Contact"
    assert body["is_active"] is False
    assert body["company_name"] == "Acme Ltd"


def test_delete_supplier(client, admin_headers, supplier):
    response = client.delete(f"{URL}{supplier['supplier_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{supplier['supplier_id']}", headers=admin_headers).status_code == 404


def test_cannot_delete_supplier_used_by_a_product(client, admin_headers, supplier, product):
    response = client.delete(f"{URL}{supplier['supplier_id']}", headers=admin_headers)

    assert response.status_code == 409


def test_invalid_email_returns_422(client, admin_headers):
    response = client.post(
        URL, json=supplier_payload(email="not-an-email"), headers=admin_headers
    )

    assert response.status_code == 422


def test_update_with_invalid_email_returns_422(client, admin_headers, supplier):
    response = client.put(
        f"{URL}{supplier['supplier_id']}", json={"email": "nope"}, headers=admin_headers
    )

    assert response.status_code == 422


def test_missing_company_name_returns_422(client, admin_headers):
    payload = supplier_payload()
    del payload["company_name"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 422


def test_blank_phone_returns_422(client, admin_headers):
    response = client.post(URL, json=supplier_payload(phone_number=" "), headers=admin_headers)

    assert response.status_code == 422