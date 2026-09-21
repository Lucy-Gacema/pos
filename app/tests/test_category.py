from tests.helpers import category_payload

URL = "/categories/"


def test_create_category(client, admin_headers):
    response = client.post(URL, json=category_payload(), headers=admin_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["category_id"] > 0
    assert body["category_name"] == "Drinks"
    assert body["is_active"] is True


def test_cashier_can_create_category(client, cashier_headers):
    response = client.post(URL, json=category_payload(), headers=cashier_headers)

    assert response.status_code == 201


def test_is_active_defaults_to_true(client, admin_headers):
    response = client.post(URL, json={"category_name": "Snacks"}, headers=admin_headers)

    assert response.status_code == 201
    assert response.json()["is_active"] is True


def test_name_is_trimmed(client, admin_headers):
    response = client.post(
        URL, json=category_payload(category_name="  Bakery  "), headers=admin_headers
    )

    assert response.json()["category_name"] == "Bakery"


def test_list_categories(client, admin_headers, category):
    response = client.get(URL, headers=admin_headers)

    assert response.status_code == 200
    assert [c["category_id"] for c in response.json()] == [category["category_id"]]


def test_get_category(client, admin_headers, category):
    response = client.get(f"{URL}{category['category_id']}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == category


def test_update_category_partially(client, admin_headers, category):
    response = client.put(
        f"{URL}{category['category_id']}",
        json={"category_name": "Beverages"},
        headers=admin_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["category_name"] == "Beverages"
    assert body["is_active"] is True  # not overwritten


def test_deactivate_category(client, admin_headers, category):
    response = client.put(
        f"{URL}{category['category_id']}", json={"is_active": False}, headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_delete_category(client, admin_headers, category):
    response = client.delete(f"{URL}{category['category_id']}", headers=admin_headers)

    assert response.status_code == 204
    assert client.get(f"{URL}{category['category_id']}", headers=admin_headers).status_code == 404


def test_cannot_delete_category_used_by_a_product(client, admin_headers, category, product):
    response = client.delete(f"{URL}{category['category_id']}", headers=admin_headers)

    assert response.status_code == 409
    # the category is still there
    assert client.get(f"{URL}{category['category_id']}", headers=admin_headers).status_code == 200


def test_missing_name_returns_422(client, admin_headers):
    response = client.post(URL, json={"is_active": True}, headers=admin_headers)

    assert response.status_code == 422


def test_empty_name_returns_422(client, admin_headers):
    response = client.post(URL, json=category_payload(category_name=""), headers=admin_headers)

    assert response.status_code == 422


def test_blank_name_returns_422(client, admin_headers):
    response = client.post(URL, json=category_payload(category_name="   "), headers=admin_headers)

    assert response.status_code == 422


def test_invalid_is_active_returns_422(client, admin_headers):
    response = client.post(URL, json=category_payload(is_active="maybe"), headers=admin_headers)

    assert response.status_code == 422


def test_update_with_blank_name_returns_422(client, admin_headers, category):
    response = client.put(
        f"{URL}{category['category_id']}", json={"category_name": " "}, headers=admin_headers
    )

    assert response.status_code == 422