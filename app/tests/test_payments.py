from tests.helpers import dec, payment_payload

URL = "/payments/"


def test_create_payment(client, admin_headers, sale):
    response = client.post(URL, json=payment_payload(sale["sale_id"]), headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["payment_id"] > 0
    assert body["sale_id"] == sale["sale_id"]
    assert body["payment_method"] == "cash"
    assert dec(body["amount_paid"]) == dec("10.00")
    assert body["payment_date"].startswith("2026-01-15T10:31:00")


def test_a_sale_can_have_several_payments(client, admin_headers, sale):
    first = client.post(
        URL, json=payment_payload(sale["sale_id"], amount_paid="4.00"), headers=admin_headers
    )
    second = client.post(
        URL,
        json=payment_payload(sale["sale_id"], payment_method="card", amount_paid="6.00"),
        headers=admin_headers,
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert len(client.get(URL, headers=admin_headers).json()) == 2


def test_get_payment(client, admin_headers, sale):
    created = client.post(
        URL, json=payment_payload(sale["sale_id"]), headers=admin_headers
    ).json()

    response = client.get(f"{URL}{created['payment_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == created


def test_update_payment(client, admin_headers, sale):
    created = client.post(
        URL, json=payment_payload(sale["sale_id"]), headers=admin_headers
    ).json()

    response = client.put(
        f"{URL}{created['payment_id']}",
        json={"payment_method": "card", "amount_paid": "12.50"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["payment_method"] == "card"
    assert dec(body["amount_paid"]) == dec("12.50")
    assert body["sale_id"] == sale["sale_id"]


def test_delete_payment(client, admin_headers, sale):
    created = client.post(
        URL, json=payment_payload(sale["sale_id"]), headers=admin_headers
    ).json()

    response = client.delete(f"{URL}{created['payment_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{created['payment_id']}", headers=admin_headers).status_code == 404


# ---------------- validation and conflicts ----------------

def test_zero_amount_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"], amount_paid="0")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_amount_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"], amount_paid="-5.00")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_amount_with_too_many_decimals_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"], amount_paid="1.234")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_missing_payment_method_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"])
    del payload["payment_method"]

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_blank_payment_method_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"], payment_method="  ")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_invalid_date_returns_422(client, admin_headers, sale):
    payload = payment_payload(sale["sale_id"], payment_date="not-a-date")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_unknown_sale_returns_409(client, admin_headers):
    response = client.post(URL, json=payment_payload(9999), headers=admin_headers)

    assert response.status_code == 409


def test_update_with_zero_amount_returns_422(client, admin_headers, sale):
    created = client.post(
        URL, json=payment_payload(sale["sale_id"]), headers=admin_headers
    ).json()

    response = client.put(
        f"{URL}{created['payment_id']}", json={"amount_paid": "0"}, headers=admin_headers
    )

    assert response.status_code == 422