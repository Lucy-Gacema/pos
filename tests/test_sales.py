from tests.helpers import create_ok, dec, receipt_payload, sale_item_payload, sale_payload

URL = "/sales/"


def test_create_sale(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"])

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["sale_id"] > 0
    assert body["user_id"] == admin_user.user_id
    assert body["customer_id"] is None
    assert dec(body["total_amount"]) == dec("10.00")
    assert dec(body["tax_amount"]) == dec("2.10")
    assert body["payment_status"] == "paid"
    assert body["receipt_number"] == receipt["receipt_number"]
    assert body["sale_date"].startswith("2026-01-15T10:30:00")


def test_create_sale_for_a_customer(client, admin_headers, admin_user, receipt, customer):
    payload = sale_payload(
        admin_user.user_id, receipt["receipt_number"], customer_id=customer["customer_id"]
    )

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    assert response.json()["customer_id"] == customer["customer_id"]


def test_discount_and_tax_default_to_zero(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"])
    del payload["discount_amount"]
    del payload["tax_amount"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    assert dec(response.json()["discount_amount"]) == 0
    assert dec(response.json()["tax_amount"]) == 0


def test_list_sales(client, admin_headers, sale):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert [s["sale_id"] for s in response.json()] == [sale["sale_id"]]


def test_get_sale(client, admin_headers, sale):
    response = client.get(f"{URL}{sale['sale_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == sale


def test_update_sale(client, admin_headers, sale):
    response = client.put(
        f"{URL}{sale['sale_id']}",
        json={"payment_status": "refunded", "discount_amount": "1.50"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["payment_status"] == "refunded"
    assert dec(body["discount_amount"]) == dec("1.50")
    assert dec(body["total_amount"]) == dec("10.00")  # untouched


def test_delete_sale(client, admin_headers, sale):
    response = client.delete(f"{URL}{sale['sale_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{sale['sale_id']}", headers=admin_headers).status_code == 404


def test_cannot_delete_sale_that_has_items(client, admin_headers, sale, product):
    create_ok(
        client,
        "/sale-items/",
        sale_item_payload(sale["sale_id"], product["product_id"]),
        admin_headers,
    )

    response = client.delete(f"{URL}{sale['sale_id']}", headers=admin_headers)

    assert response.status_code == 409
    assert client.get(f"{URL}{sale['sale_id']}", headers=admin_headers).status_code == 200



def test_unknown_user_returns_409(client, admin_headers, receipt):
    payload = sale_payload(9999, receipt["receipt_number"])

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_unknown_customer_returns_409(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"], customer_id=9999)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_unknown_receipt_returns_409(client, admin_headers, admin_user):
    payload = sale_payload(admin_user.user_id, "NO-SUCH-RECEIPT")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_receipt_cannot_be_used_by_two_sales(client, admin_headers, admin_user, sale):
    payload = sale_payload(admin_user.user_id, sale["receipt_number"])

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_second_sale_with_its_own_receipt_is_fine(client, admin_headers, admin_user, sale):
    create_ok(client, "/receipts/", receipt_payload(receipt_number="R-0002"), admin_headers)
    payload = sale_payload(admin_user.user_id, "R-0002")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 201


def test_negative_total_returns_422(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"], total_amount="-5.00")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_discount_returns_422(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"], discount_amount="-1")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_missing_receipt_number_returns_422(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"])
    del payload["receipt_number"]

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_invalid_date_returns_422(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"], sale_date="yesterday")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_blank_payment_status_returns_422(client, admin_headers, admin_user, receipt):
    payload = sale_payload(admin_user.user_id, receipt["receipt_number"], payment_status=" ")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_update_with_negative_total_returns_422(client, admin_headers, sale):
    response = client.put(
        f"{URL}{sale['sale_id']}", json={"total_amount": "-1"}, headers=admin_headers
    )

    assert response.status_code == 422