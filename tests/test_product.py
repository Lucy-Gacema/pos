from tests.helpers import dec, product_payload

URL = "/products/"


def test_list_products_empty(client, admin_headers):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_create_product(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"])

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] > 0
    assert body["product_name"] == "Cola"
    assert body["barcode"] == "5449000000096"
    assert dec(body["selling_price"]) == dec("1.99")
    assert body["in_stock"] == 100
    assert body["category_id"] == category["category_id"]
    assert body["supplier_id"] == supplier["supplier_id"]


def test_list_products(client, admin_headers, product):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert [p["product_id"] for p in response.json()] == [product["product_id"]]


def test_get_product(client, admin_headers, product):
    response = client.get(f"{URL}{product['product_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == product


def test_update_product_partially(client, admin_headers, product):
    response = client.put(
        f"{URL}{product['product_id']}",
        json={"in_stock": 55, "selling_price": "2.49"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["in_stock"] == 55
    assert dec(body["selling_price"]) == dec("2.49")
    assert body["product_name"] == "Cola"  # untouched field is preserved
    assert body["barcode"] == product["barcode"]


def test_delete_product(client, admin_headers, product):
    response = client.delete(f"{URL}{product['product_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{product['product_id']}", headers=admin_headers).status_code == 404


def test_cannot_delete_product_that_was_sold(client, admin_headers, product, sale):
    from tests.helpers import sale_item_payload

    client.post(
        "/sale-items/",
        json=sale_item_payload(sale["sale_id"], product["product_id"]),
        headers=admin_headers,
    )

    response = client.delete(f"{URL}{product['product_id']}", headers=admin_headers)

    assert response.status_code == 409



def test_duplicate_barcode_returns_409(client, admin_headers, product):
    payload = product_payload(
        product["category_id"], product["supplier_id"], product_name="Other"
    )

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 409


def test_update_to_existing_barcode_returns_409(client, admin_headers, product):
    other = client.post(
        URL,
        json=product_payload(product["category_id"], product["supplier_id"], barcode="111"),
        headers=admin_headers,
    ).json()

    response = client.put(
        f"{URL}{other['product_id']}", json={"barcode": product["barcode"]}, headers=admin_headers
    )

    assert response.status_code == 409


def test_unknown_category_returns_409(client, admin_headers, supplier):
    payload = product_payload(9999, supplier["supplier_id"])

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 409


def test_unknown_supplier_returns_409(client, admin_headers, category):
    payload = product_payload(category["category_id"], 9999)

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 409


def test_update_to_unknown_category_returns_409(client, admin_headers, product):
    response = client.put(
        f"{URL}{product['product_id']}", json={"category_id": 9999}, headers=admin_headers
    )

    assert response.status_code == 409


def test_missing_required_field_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"])
    del payload["barcode"]

    response = client.post(URL, json=payload, headers=admin_headers)

    assert response.status_code == 422


def test_empty_body_returns_422(client, admin_headers):
    response = client.post(URL, json={}, headers=admin_headers)

    assert response.status_code == 422


def test_negative_price_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], selling_price="-1.00")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_zero_price_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], selling_price="0")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_price_with_too_many_decimals_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], selling_price="1.999")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_non_numeric_price_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], selling_price="cheap")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_stock_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], in_stock=-1)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_negative_reorder_level_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], reorder_level=-1)

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_blank_name_returns_422(client, admin_headers, category, supplier):
    payload = product_payload(category["category_id"], supplier["supplier_id"], product_name="  ")

    assert client.post(URL, json=payload, headers=admin_headers).status_code == 422


def test_update_with_negative_stock_returns_422(client, admin_headers, product):
    response = client.put(
        f"{URL}{product['product_id']}", json={"in_stock": -5}, headers=admin_headers
    )

    assert response.status_code == 422