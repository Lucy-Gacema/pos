def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "active" in body["message"]


def test_unknown_route_returns_404(client):
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404


def test_openapi_schema_is_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/products/" in response.json()["paths"]