from tests.helpers import dec, sale_item_payload

URL = "/sale-items/"


def test_create_sale_item(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"])

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["sale_item_id"] > 0
    assert body["sale_id"] == sale["sale_id"]
    assert body["product_id"] == product["product_id"]
    assert body["quantity"] == 2
    assert dec(body["unit_price"]) == dec("1.99")
    assert dec(body["sub_total"]) == dec("3.98")


def test_sub_total_is_computed_not_trusted(client, admin_headers, sale, product):
    payload = sale_item_payload(
        sale["sale_id"], product["product_id"], quantity=3, unit_price="2.50", sub_total="999.99"
    )

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    assert dec(response.json()["sub_total"]) == dec("7.50")


def test_list_sale_items(client, admin_headers, sale, product):
    client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    )

    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_sale_item(client, admin_headers, sale, product):
    created = client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    ).json()

    response = client.get(f"{URL}{created['sale_item_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == created


def test_update_quantity_recomputes_sub_total(client, admin_headers, sale, product):
    created = client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    ).json()

    response = client.put(
        f"{URL}{created['sale_item_id']}", json={"quantity": 5}, headers=admin_headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["quantity"] == 5
    assert dec(body["sub_total"]) == dec("9.95")


def test_update_unit_price_recomputes_sub_total(client, admin_headers, sale, product):
    created = client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    ).json()

    response = client.put(
        f"{URL}{created['sale_item_id']}", json={"unit_price": "3.00"}, headers=admin_headers
    )

    assert response.status_code == 200
    assert dec(response.json()["sub_total"]) == dec("6.00")


def test_delete_sale_item(client, admin_headers, sale, product):
    created = client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    ).json()

    response = client.delete(f"{URL}{created['sale_item_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{created['sale_item_id']}", headers=admin_headers).status_code == 404


# ---------------- validation and conflicts ----------------

def test_zero_quantity_returns_422(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"], quantity=0)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_quantity_returns_422(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"], quantity=-3)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_unit_price_returns_422(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"], unit_price="-1.00")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_non_integer_quantity_returns_422(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"], quantity="many")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_missing_product_id_returns_422(client, admin_headers, sale, product):
    payload = sale_item_payload(sale["sale_id"], product["product_id"])
    del payload["product_id"]

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_unknown_sale_returns_409(client, admin_headers, product):
    payload = sale_item_payload(9999, product["product_id"])

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_unknown_product_returns_409(client, admin_headers, sale):
    payload = sale_item_payload(sale["sale_id"], 9999)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 409


def test_update_with_zero_quantity_returns_422(client, admin_headers, sale, product):
    created = client.post(
        URL, json=sale_item_payload(sale["sale_id"], product["product_id"]), headers=admin_headers
    ).json()

    response = client.put(
        f"{URL}{created['sale_item_id']}", json={"quantity": 0}, headers=admin_headers
    )

    assert response.status_code == 422