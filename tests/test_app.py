import app as application

def test_home_redirects_to_register():
    client = application.app.test_client()
    response = client.get("/")
    assert response.status_code == 302
    assert "/register" in response.headers["Location"]

def test_health_route_exists():
    client = application.app.test_client()
    response = client.get("/health")
    assert response.status_code in (200, 503)
