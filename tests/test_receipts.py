from tests.helpers import receipt_payload

URL = "/receipts/"


def test_create_receipt(client, admin_headers):
    response = client.post(URL, json=receipt_payload(), headers=admin_headers)

    assert response.status_code == 201
    assert response.json() == {"receipt_number": "R-0001", "is_printed": False}


def test_is_printed_defaults_to_false(client, admin_headers):
    response = client.post(URL, json={"receipt_number": "R-9"}, headers=admin_headers)

    assert response.status_code == 201
    assert response.json()["is_printed"] is False


def test_list_receipts(client, admin_headers, receipt):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == [receipt]


def test_get_receipt_by_number(client, admin_headers, receipt):
    response = client.get(f"{URL}{receipt['receipt_number']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == receipt


def test_mark_receipt_as_printed(client, admin_headers, receipt):
    response = client.put(
        f"{URL}{receipt['receipt_number']}", json={"is_printed": True}, headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["is_printed"] is True


def test_receipt_number_cannot_be_changed(client, admin_headers, receipt):
    response = client.put(
        f"{URL}{receipt['receipt_number']}",
        json={"receipt_number": "HACKED", "is_printed": True},
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["receipt_number"] == "R-0001"
    assert client.get(f"{URL}HACKED", headers=admin_headers).status_code == 404


def test_delete_receipt(client, admin_headers, receipt):
    response = client.delete(f"{URL}{receipt['receipt_number']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{receipt['receipt_number']}", headers=admin_headers).status_code == 404


def test_cannot_delete_receipt_used_by_a_sale(client, admin_headers, receipt, sale):
    response = client.delete(f"{URL}{receipt['receipt_number']}", headers=admin_headers)

    assert response.status_code == 409


def test_duplicate_receipt_number_returns_409(client, admin_headers, receipt):
    response = client.post(URL, json=receipt_payload(), headers=admin_headers)

    assert response.status_code == 409


def test_missing_receipt_number_returns_422(client, admin_headers):
    response = client.post(URL, json={"is_printed": True}, headers=admin_headers)

    assert response.status_code == 422


def test_blank_receipt_number_returns_422(client, admin_headers):
    response = client.post(URL, json=receipt_payload(receipt_number="  "), headers=admin_headers)

    assert response.status_code == 422


def test_invalid_is_printed_returns_422(client, admin_headers):
    response = client.post(URL, json=receipt_payload(is_printed="maybe"), headers=admin_headers)

    assert response.status_code == 422