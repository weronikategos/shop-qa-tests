import pytest

pytestmark = pytest.mark.api


def test_health_returns_ok(api):
    """TC-API-01"""
    response = api.get(f"{api.base_url}/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_responds_quickly(api):
    """TC-API-02: a simple performance check, response under 500 ms"""
    response = api.get(f"{api.base_url}/api/health")
    assert response.elapsed.total_seconds() < 0.5
