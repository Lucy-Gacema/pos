import pytest

COLLECTIONS = [
    "/categories/",
    "/suppliers/",
    "/customers/",
    "/products/",
    "/receipts/",
    "/sales/",
    "/sale-items/",
    "/payments/",
]

INTEGER_ID_COLLECTIONS = [url for url in COLLECTIONS if url != "/receipts/"]


@pytest.mark.parametrize("url", COLLECTIONS)
class TestWithoutToken:
    def test_list_returns_401(self, client, url):
        assert client.get(url).status_code == 401

    def test_create_returns_401(self, client, url):
        assert client.post(url, json={}).status_code == 401

    def test_get_one_returns_401(self, client, url):
        assert client.get(f"{url}1").status_code == 401

    def test_update_returns_401(self, client, url):
        assert client.put(f"{url}1", json={}).status_code == 401

    def test_delete_returns_401(self, client, url):
        assert client.delete(f"{url}1").status_code == 401


@pytest.mark.parametrize("url", COLLECTIONS)
def test_invalid_token_returns_401(client, url):
    response = client.get(url, headers={"Authorization": "Bearer not-a-real-token"})

    assert response.status_code == 401


@pytest.mark.parametrize("url", COLLECTIONS)
def test_cashier_can_list(client, cashier_headers, url):
    response = client.get(url, headers=cashier_headers)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("url", COLLECTIONS)
def test_cashier_cannot_delete(client, cashier_headers, url):
    response = client.delete(f"{url}1", headers=cashier_headers)

    assert response.status_code == 403


@pytest.mark.parametrize("url", COLLECTIONS)
class TestMissingRecords:
    def test_get_missing_returns_404(self, client, admin_headers, url):
        response = client.get(f"{url}999", headers=admin_headers)

        assert response.status_code == 404
        assert response.json()["detail"].endswith("not found")

    def test_update_missing_returns_404(self, client, admin_headers, url):
        response = client.put(f"{url}999", json={}, headers=admin_headers)

        assert response.status_code == 404

    def test_delete_missing_returns_404(self, client, admin_headers, url):
        response = client.delete(f"{url}999", headers=admin_headers)

        assert response.status_code == 404


@pytest.mark.parametrize("url", INTEGER_ID_COLLECTIONS)
def test_non_integer_id_returns_422(client, admin_headers, url):
    response = client.get(f"{url}abc", headers=admin_headers)

    assert response.status_code == 422
