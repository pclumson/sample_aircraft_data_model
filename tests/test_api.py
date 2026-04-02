import pytest
from fastapi.testclient import TestClient
from ..api.main import app
from ..models.database import get_database_engine, init_db, Base, sessionmaker

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Setup test database before each test."""
    engine = get_database_engine("sqlite:///:memory:")
    init_db(engine)
    app.state.engine = engine
    yield
    Base.metadata.drop_all(engine)


class TestComponentAPI:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "Aircraft Component Data API" in response.json()["message"]

    def test_create_component(self):
        payload = {
            "name": "Test Component",
            "material": "aluminum",
            "dimensions": {
                "length": 2.5,
                "width": 0.3,
                "height": 0.15,
                "tolerance": 0.0005
            },
            "mass": 45.7,
            "version": "1.0.0"
        }
        response = client.post("/api/v1/components/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "component_id" in data["data"]

    def test_list_components(self):
        response = client.get("/api/v1/components/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_nonexistent_component(self):
        response = client.get("/api/v1/components/nonexistent-id")
        assert response.status_code == 404

    def test_delete_component(self):
        # First create a component
        payload = {
            "name": "Delete Test",
            "material": "aluminum",
            "dimensions": {"length": 1.0, "width": 1.0, "height": 1.0},
            "mass": 10.0
        }
        create_response = client.post("/api/v1/components/", json=payload)
        component_id = create_response.json()["data"]["component_id"]

        # Delete it
        response = client.delete(f"/api/v1/components/{component_id}")
        assert response.status_code == 200
        assert response.json()["success"] is True
